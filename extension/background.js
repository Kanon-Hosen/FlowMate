// FlowMate Chrome Extension Background Service Worker (Manifest V3)

let cachedState = {
  connected: false,
  active_project: null,
  enabled: true
};

// Poll local FlowMate desktop app API on http://127.0.0.1:18420
async function updateDesktopState() {
  try {
    const res = await fetch("http://127.0.0.1:18420/status", { cache: "no-store" });
    if (res.ok) {
      const data = await res.json();
      cachedState.connected = true;
      cachedState.active_project = data.active_project;
      cachedState.all_projects = data.all_projects;
    } else {
      cachedState.connected = false;
    }
  } catch (err) {
    cachedState.connected = false;
  }
}

// Initial fetch & periodic poll every 2.5 seconds
updateDesktopState();
setInterval(updateDesktopState, 2500);

// Helper to format dynamic templates synchronously
function renderTemplate(template, counter, padding, project, origName, ext) {
  if (!template || !template.trim()) template = "{counter}";
  
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0]; // YYYY-MM-DD
  const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-'); // HH-MM-SS
  const paddedCounter = String(counter).padStart(padding || 3, '0');
  
  const origBase = origName.replace(/\.[^/.]+$/, "");
  const extClean = ext.replace(/^\./, "");

  let result = template
    .replace(/{counter}/g, paddedCounter)
    .replace(/{project}/g, (project || "Project").replace(/[\\/*?:"<>|]/g, "_"))
    .replace(/{date}/g, dateStr)
    .replace(/{time}/g, timeStr)
    .replace(/{original}/g, origBase.replace(/[\\/*?:"<>|]/g, "_"))
    .replace(/{ext}/g, extClean);

  result = result.replace(/[\\/*?:"<>|]/g, "_").trim();
  const extSuffix = extClean ? `.${extClean}` : "";
  if (!result.toLowerCase().endsWith(extSuffix.toLowerCase())) {
    result += extSuffix;
  }
  return result;
}

// SYNCHRONOUS Download Filename Interceptor
chrome.downloads.onDeterminingFilename.addListener((item, suggest) => {
  if (!cachedState.enabled) {
    suggest();
    return true;
  }

  const filename = item.filename || "";
  const ext = filename.split('.').pop() || "";
  const isTargetMedia = ['mp4', 'webm', 'mkv', 'mov', 'avi', 'png', 'jpg', 'jpeg', 'zip', 'rar'].includes(ext.toLowerCase());

  if (isTargetMedia && cachedState.active_project) {
    const proj = cachedState.active_project;
    const template = proj.name_template || "{counter}";
    
    const formattedName = renderTemplate(
      template,
      proj.current_counter,
      proj.padding_digits || 3,
      proj.name,
      filename,
      ext
    );

    // Record activity log in Chrome extension storage
    chrome.storage.local.get({ downloadHistory: [] }, (res) => {
      const history = res.downloadHistory;
      history.unshift({
        time: new Date().toLocaleTimeString(),
        original: filename,
        new_name: formattedName,
        project: proj.name
      });
      chrome.storage.local.set({ downloadHistory: history.slice(0, 20) });
    });

    // Increment local counter prediction for next fast download
    proj.current_counter += 1;

    // Suggest new filename directly in Chrome
    suggest({ filename: `FlowMate_Output/${formattedName}` });
  } else {
    suggest();
  }

  return true; // Keep suggestion listener active
});
