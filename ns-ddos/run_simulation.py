<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="../inc/bootstrap.min.css">
    <link rel="stylesheet" href="../inc/gauge.css">
    <link rel="stylesheet" href="css/app.css"></script>
    <script type="text/javascript" src="../inc/jquery.min.js"></script>
    <script type="text/javascript" src="../inc/jquery.widget.js"></script>
    <script type="text/javascript" src="../inc/jquery.gauge.js"></script>
    <script type="text/javascript" src="../inc/popper.min.js"></script>
    <script type="text/javascript" src="../inc/bootstrap.min.js"></script>
    <script type="text/javascript" src="js/app.js"></script>
    <title>NS-DDOS</title>
  </head>
  <body>



    <div id="metric-sflow-bps"></div>
<div id="metric-sflow-pps"></div>
<div id="metric-heap"></div>
<!-- ... add the rest accordingly ... -->

    <nav class="navbar navbar-expand-md navbar-dark mb-3" style="background-color: rgb(245, 80, 9);">
      <a class="navbar-brand" href="">
        <img src="" height="30" class="d-inline-block align-top">
        NS
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item" data-toggle="collapse" data-target=".navbar-collapse.show">
            <a class="nav-link" href="#" data-target="status">Status</a>
          </li>
          <li class="nav-item" data-toggle="collapse" data-target=".navbar-collapse.show">
            <a class="nav-link" href="#" data-target="apps">Apps</a>
          </li>
        </ul>
      </div>
    </nav>
    <main class="container" role="main">

      <section id="status">
        <div class="row align-items-center">
          <div class="col-md"><div id="metric-agents"></div></div>
          <div class="col-md"><div id="metric-sflow-bps"></div></div>
          <div class="col-md"><div id="metric-sflow-pps"></div></div>
        </div>
        <div class="row align-items-center">
          <div class="col-md"><div id="metric-app-run"></div></div>
          <div class="col-md"><div id="metric-app-err"></div></div>
          <div class="col-md"><div id="metric-cpu-process"></div></div>
        </div>
        <div class="row align-items-center">
          <div class="col-md"><div id="metric-script-run"></div></div>
          <div class="col-md"><div id="metric-script-err"></div></div>
          <div class="col-md"><div id="metric-cpu-system"></div></div>
        </div>
        <div class="row align-items-center">
          <div class="col-md"><div id="metric-http-conn-cur"></div></div>
          <div class="col-md"><div id="metric-http-conn-tot"></div></div>
          <div class="col-md"><div id="metric-heap"></div></div>
        </div>
      </section>

      <section id="apps">
<h3>Installed Applications</h3>
  <p>Click on an application in the list to access the application's home page:</p>
    <div id="app-list" class="mb-3"></div>
  <p>Visit <a href="">Applications</a> for information on downloading applications.</p>
  </div>
      </section>

      <section id="api">
      </section>
      <section id="license">
</ol>
    </section>

      <section id="about" class="container">
<table class="table table-striped table-bordered table-sm" id="about-info">
<tbody>
</tbody>
</table>
      </section>

    </main>

    <footer class="footer page-footer border-top mt-3">
       <div class="footer-copyright text-center py-2">
         <small class="text-muted">Copyright &copy; 2025-<span class="year">2025</span> NS 0Done by Dev 0Deen. ALL RIGHTS RESERVED</small>
       </div>
    </footer>
  </body>
</html>


