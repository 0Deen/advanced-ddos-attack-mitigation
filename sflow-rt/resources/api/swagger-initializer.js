window.onload = function() {
  function HideComponentsPlugin() {
    // override disabled components to return nothing
    return {
      components: {
        Topbar: function() { return null; },
        CopyToClipboardBtn: function() { return null; }
      }
    };
  };

  // Build a system
  window.ui = SwaggerUIBundle({
    url: "../api-docs",
    validatorUrl: null,
    dom_id: '#swagger-ui',
    deepLinking: false,
    docExpansion: 'none',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl,
      HideComponentsPlugin
    ],
    layout: "StandaloneLayout",
    tagsSorter: "alpha",
    operationsSorter: "alpha"
  });
};
