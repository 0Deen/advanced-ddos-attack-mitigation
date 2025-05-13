# controller/controller.py

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from collections import defaultdict

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Anomaly thresholds (basic prototype)
THRESHOLD_PACKET_RATE = 1000
BLACKLIST = set()
TRAFFIC_LOG = defaultdict(list)

# Attack signatures (can be replaced with ML-based classifier)
DDOS_SIGNATURES = {
    "ICMP Flood": {"protocol": "ICMP", "rate": ">1000/s"},
    "SYN Flood": {"flags": "S", "rate": ">1000/s"},
    "UDP Flood": {"protocol": "UDP", "rate": ">1000/s"},
    "HTTP Flood": {"port": 80, "method": "GET", "rate": ">500/s"},
    "Nping TCP Flood": {"tool": "nping", "rate": ">1000/s"},
}

class SimpleController(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        src_ip = str(packet.src)
        dst_ip = str(packet.dst)

        now = time.time()
        TRAFFIC_LOG[src_ip].append(now)
        TRAFFIC_LOG[src_ip] = [t for t in TRAFFIC_LOG[src_ip] if now - t < 1]

        pkt_rate = len(TRAFFIC_LOG[src_ip])
        if pkt_rate > THRESHOLD_PACKET_RATE:
            if src_ip not in BLACKLIST:
                log.warning("🔴 DDoS attack suspected from %s!", src_ip)
                BLACKLIST.add(src_ip)
                self.block_ip(src_ip)
        else:
            self.forward_packet(event)

    def forward_packet(self, event):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        msg.in_port = event.port
        self.connection.send(msg)

    def block_ip(self, ip):
        msg = of.ofp_flow_mod()
        msg.match.dl_src = ip
        msg.actions = []
        self.connection.send(msg)


def launch():
    def start_switch(event):
        log.info("🔌 Controller connected to switch: %s", event.connection)
        SimpleController(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
    log.info("✅ SDN Controller running (Standalone Python)")
