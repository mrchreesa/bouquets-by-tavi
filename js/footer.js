// Runs after the deferred analytics installer; the consent prompt stays available.
(function () {
  var host = document.getElementById("webm8-privacy");
  var button = host && host.shadowRoot && host.shadowRoot.querySelector(".preferences");
  if (!button) return;
  button.hidden = true;
  host.style.padding = "0";
})();
