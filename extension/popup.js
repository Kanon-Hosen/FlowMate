document.addEventListener('DOMContentLoaded', () => {
  const connectionBadge = document.getElementById('connectionBadge');
  const projectSelect = document.getElementById('projectSelect');
  const templateInput = document.getElementById('templateInput');
  const previewBox = document.getElementById('previewBox');
  const counterVal = document.getElementById('counterVal');
  const todayVal = document.getElementById('todayVal');
  const totalVal = document.getElementById('totalVal');
  const autoToggle = document.getElementById('autoToggle');
  const historyList = document.getElementById('historyList');

  // Load extension state
  chrome.storage.local.get({ autoRename: true, downloadHistory: [] }, (res) => {
    autoToggle.checked = res.autoRename;
    renderHistory(res.downloadHistory);
  });

  autoToggle.addEventListener('change', () => {
    chrome.storage.local.set({ autoRename: autoToggle.checked });
  });

  // Fetch status from local FlowMate desktop app
  async function fetchStatus() {
    try {
      const res = await fetch("http://127.0.0.1:18420/status", { cache: "no-store" });
      if (res.ok) {
        const data = await res.json();
        connectionBadge.className = "status-badge status-online";
        connectionBadge.innerText = "● Desktop Connected";

        if (data.all_projects && data.active_project) {
          updateProjectDropdown(data.all_projects, data.active_project.id);
          updateProjectDetails(data.active_project);
        }
      } else {
        setOffline();
      }
    } catch (e) {
      setOffline();
    }
  }

  function setOffline() {
    connectionBadge.className = "status-badge status-offline";
    connectionBadge.innerText = "● Desktop Offline";
  }

  function updateProjectDropdown(allProjects, activeId) {
    projectSelect.innerHTML = "";
    allProjects.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.innerText = p.name;
      if (p.id === activeId) opt.selected = true;
      projectSelect.appendChild(opt);
    });
  }

  function updateProjectDetails(proj) {
    const template = proj.name_template || "{counter}";
    templateInput.value = template;
    const padding = proj.padding_digits || 3;
    const padded = String(proj.current_counter).padStart(padding, '0');
    
    counterVal.innerText = padded;
    todayVal.innerText = proj.files_today || 0;
    totalVal.innerText = proj.files_total || 0;

    previewBox.innerText = `Preview: ${padded}.mp4`;
  }

  projectSelect.addEventListener('change', async () => {
    const selectedId = projectSelect.value;
    if (!selectedId) return;

    try {
      await fetch("http://127.0.0.1:18420/api/switch_project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id: selectedId })
      });
      fetchStatus();
    } catch (e) {
      console.error("Project switch error:", e);
    }
  });

  function renderHistory(history) {
    if (!history || history.length === 0) {
      historyList.innerHTML = '<div style="color: #64748B; text-align: center; padding: 8px;">No recent download activity</div>';
      return;
    }

    historyList.innerHTML = "";
    history.forEach(item => {
      const div = document.createElement("div");
      div.className = "history-item";
      div.innerHTML = `
        <span class="orig" title="${item.original}">${item.original}</span>
        <span class="renamed">➜ ${item.new_name}</span>
      `;
      historyList.appendChild(div);
    });
  }

  // Initial fetch and poll
  fetchStatus();
  setInterval(fetchStatus, 2000);
});
