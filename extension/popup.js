document.addEventListener('DOMContentLoaded', () => {
  const templateInput = document.getElementById('templateInput');
  const prefixInput = document.getElementById('prefixInput');
  const saveBtn = document.getElementById('saveBtn');

  // Load saved extension preferences
  chrome.storage.sync.get(['nameTemplate', 'customPrefix'], (data) => {
    if (data.nameTemplate) templateInput.value = data.nameTemplate;
    if (data.customPrefix) prefixInput.value = data.customPrefix;
  });

  saveBtn.addEventListener('click', () => {
    chrome.storage.sync.set({
      nameTemplate: templateInput.value,
      customPrefix: prefixInput.value
    }, () => {
      saveBtn.innerText = 'Saved!';
      setTimeout(() => { saveBtn.innerText = 'Save Settings'; }, 1500);
    });
  });
});
