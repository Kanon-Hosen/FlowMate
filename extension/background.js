// FlowMate Chrome Extension Background Service Worker (Manifest V3)

chrome.downloads.onDeterminingFilename.addListener((item, suggest) => {
  // Read user extension preferences
  chrome.storage.sync.get(['nameTemplate', 'customPrefix'], (data) => {
    const template = data.nameTemplate || '{counter}';
    const prefix = data.customPrefix || '';
    
    const ext = item.filename.split('.').pop();
    const isVideo = ['mp4', 'webm', 'mkv', 'mov', 'avi'].includes(ext.toLowerCase());

    if (isVideo && prefix) {
      // Suggest clean formatted name directly inside Chrome
      const sanitizedPrefix = prefix.replace(/[^a-zA-Z0-9_-]/g, '_');
      suggest({ filename: `FlowMate_Pending/${sanitizedPrefix}${item.filename}` });
    } else {
      suggest();
    }
  });

  return true; // Async suggestion support
});
