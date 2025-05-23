from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

import switch
from datetime import datetime

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


class SimpleMonitor13(switch.SimpleSwitch13):
    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

        start = datetime.now()
        self.flow_training()
        end = datetime.now()
        print("Training time:", (end - start))

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)
            self.flow_predict()

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        timestamp = datetime.now().timestamp()
        file0 = open("PredictFlowStatsfile.csv", "w")
        file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')
        
        body = ev.msg.body
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda f: (f.match['eth_type'], f.match['ipv4_src'], f.match['ipv4_dst'], f.match['ip_proto'])):
            ip_src = stat.match['ipv4_src']
            ip_dst = stat.match['ipv4_dst']
            ip_proto = stat.match['ip_proto']
            icmp_code = -1
            icmp_type = -1
            tp_src = 0
            tp_dst = 0

            if ip_proto == 1:  # ICMP
                icmp_code = stat.match.get('icmpv4_code', -1)
                icmp_type = stat.match.get('icmpv4_type', -1)
            elif ip_proto == 6:  # TCP
                tp_src = stat.match.get('tcp_src', 0)
                tp_dst = stat.match.get('tcp_dst', 0)
            elif ip_proto == 17:  # UDP
                tp_src = stat.match.get('udp_src', 0)
                tp_dst = stat.match.get('udp_dst', 0)

            flow_id = f"{ip_src}{tp_src}{ip_dst}{tp_dst}{ip_proto}"

            try:
                packet_count_per_second = stat.packet_count / stat.duration_sec if stat.duration_sec else 0
                packet_count_per_nsecond = stat.packet_count / stat.duration_nsec if stat.duration_nsec else 0
                byte_count_per_second = stat.byte_count / stat.duration_sec if stat.duration_sec else 0
                byte_count_per_nsecond = stat.byte_count / stat.duration_nsec if stat.duration_nsec else 0
            except:
                packet_count_per_second = packet_count_per_nsecond = 0
                byte_count_per_second = byte_count_per_nsecond = 0

            file0.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"
                        .format(timestamp, ev.msg.datapath.id, flow_id, ip_src, tp_src, ip_dst, tp_dst,
                                ip_proto, icmp_code, icmp_type, stat.duration_sec, stat.duration_nsec,
                                stat.idle_timeout, stat.hard_timeout, stat.flags, stat.packet_count,
                                stat.byte_count, packet_count_per_second, packet_count_per_nsecond,
                                byte_count_per_second, byte_count_per_nsecond))
        file0.close()

    def flow_training(self):
        self.logger.info("Flow Training ...")
        try:
            flow_dataset = pd.read_csv('FlowStatsfile.csv')

            flow_dataset.iloc[:, 2] = flow_dataset.iloc[:, 2].astype(str).str.replace('.', '', regex=False)
            flow_dataset.iloc[:, 3] = flow_dataset.iloc[:, 3].astype(str).str.replace('.', '', regex=False)
            flow_dataset.iloc[:, 5] = flow_dataset.iloc[:, 5].astype(str).str.replace('.', '', regex=False)

            X_flow = flow_dataset.iloc[:, :-1].values.astype('float64')
            y_flow = flow_dataset.iloc[:, -1].values

            X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.25, random_state=0)

            classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=0)
            self.flow_model = classifier.fit(X_flow_train, y_flow_train)

            y_flow_pred = self.flow_model.predict(X_flow_test)
            cm = confusion_matrix(y_flow_test, y_flow_pred)
            acc = accuracy_score(y_flow_test, y_flow_pred)

            self.logger.info("------------------------------------------------------------------------------")
            self.logger.info("Confusion matrix:\n%s", cm)
            self.logger.info("Success Accuracy: %.2f%%", acc * 100)
            self.logger.info("Failure Rate: %.2f%%", (1.0 - acc) * 100)
            self.logger.info("------------------------------------------------------------------------------")

        except Exception as e:
            self.logger.error("Training error: %s", str(e))

    def flow_predict(self):
        try:
            predict_flow_dataset = pd.read_csv('PredictFlowStatsfile.csv')
            predict_flow_dataset.iloc[:, 2] = predict_flow_dataset.iloc[:, 2].astype(str).str.replace('.', '', regex=False)
            predict_flow_dataset.iloc[:, 3] = predict_flow_dataset.iloc[:, 3].astype(str).str.replace('.', '', regex=False)
            predict_flow_dataset.iloc[:, 5] = predict_flow_dataset.iloc[:, 5].astype(str).str.replace('.', '', regex=False)

            X_predict_flow = predict_flow_dataset.values.astype('float64')
            y_flow_pred = self.flow_model.predict(X_predict_flow)

            legitimate_traffic = sum(1 for i in y_flow_pred if i == 0)
            ddos_traffic = len(y_flow_pred) - legitimate_traffic

            self.logger.info("------------------------------------------------------------------------------")
            if (legitimate_traffic / len(y_flow_pred) * 100) > 80:
                self.logger.info("Legitimate traffic detected.")
            else:
                self.logger.info("DDoS traffic detected.")
                for i, pred in enumerate(y_flow_pred):
                    if pred != 0:
                        victim = int(predict_flow_dataset.iloc[i, 5]) % 20
                        self.logger.info("Potential victim: host h%s", victim)
                        break
            self.logger.info("------------------------------------------------------------------------------")

            # Clear prediction file
            with open("PredictFlowStatsfile.csv", "w") as file0:
                file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')

        except Exception as e:
            self.logger.error("Prediction error: %s", str(e))
