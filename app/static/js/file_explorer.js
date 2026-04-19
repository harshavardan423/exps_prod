function viewFile(filePath) {
    fetch('/' + ATOM_USERNAME + '/file-content/' + encodeURIComponent(filePath))
        .then(function (r) { if (!r.ok) throw new Error('Not available'); return r.json(); })
        .then(function (data) { displayFileContent(data, filePath); })
        .catch(function (err) {
            document.getElementById('fv-name').textContent = filePath.split('/').pop();
            document.getElementById('fv-content').innerHTML =
                '<div style="text-align:center;color:var(--red);padding:32px;"><i class="fas fa-exclamation-triangle" style="font-size:28px;margin-bottom:10px;display:block;"></i>Failed: ' + err.message + '</div>';
            document.getElementById('fv-overlay').classList.add('open');
        });
}

function displayFileContent(data, filePath) {
    document.getElementById('fv-name').textContent = data.filename;
    var contentDiv = document.getElementById('fv-content');
    var dl = document.getElementById('fv-download');
    var newDl = dl.cloneNode(true);
    dl.parentNode.replaceChild(newDl, dl);
    document.getElementById('fv-download').addEventListener('click', function (e) {
        e.preventDefault();
        try {
            var bin;
            var isText = data.mime_type && (data.mime_type.startsWith('text/') || data.mime_type === 'application/json' || data.mime_type === 'application/javascript');
            if (isText) { try { bin = atob(data.content); } catch (x) { bin = String.fromCharCode.apply(null, new TextEncoder().encode(data.content)); } }
            else { bin = atob(data.content); }
            var bytes = new Uint8Array(bin.length);
            for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            var blob = new Blob([bytes], { type: data.mime_type || 'application/octet-stream' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a'); a.href = url; a.download = data.filename;
            document.body.appendChild(a); a.click();
            setTimeout(function () { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
        } catch (err) { alert('Download failed: ' + err.message); }
    });

    if (data.filename.endsWith('.html') || data.mime_type === 'text/html') {
        contentDiv.innerHTML = '<div class="fv-tabs"><button class="fv-tab active" id="tab-raw" onclick="switchTab(\'raw\')">Raw</button><button class="fv-tab" id="tab-render" onclick="openRendered()">Rendered <i class="fas fa-external-link-alt" style="font-size:10px;"></i></button></div><div id="fv-raw"><pre>' + escHtml(data.content) + '</pre></div>';
        window._currentHtml = data.content;
    } else if (data.mime_type && data.mime_type.startsWith('image/')) {
        contentDiv.innerHTML = '<div style="text-align:center;"><img src="data:' + data.mime_type + ';base64,' + data.content + '" style="max-width:100%;max-height:60vh;border-radius:var(--radius-sm);"></div>';
    } else if (data.mime_type && (data.mime_type.startsWith('text/') || data.mime_type === 'application/json' || data.mime_type === 'application/javascript')) {
        contentDiv.innerHTML = '<pre>' + escHtml(data.content) + '</pre>';
    } else {
        contentDiv.innerHTML = '<div style="text-align:center;padding:28px;color:var(--text-dim);"><i class="fas fa-file" style="font-size:36px;margin-bottom:10px;display:block;opacity:.35;"></i><div style="font-family:var(--mono);font-size:11px;">' + data.mime_type + '</div><div style="margin-top:8px;font-size:13px;">Use the download button to save this file.</div></div>';
    }
    document.getElementById('fv-overlay').classList.add('open');
}

function switchTab(t) {
    var raw = document.getElementById('fv-raw');
    if (raw) raw.style.display = t === 'raw' ? '' : 'none';
    var tabRaw = document.getElementById('tab-raw');
    if (tabRaw) tabRaw.classList.toggle('active', t === 'raw');
}
function openRendered() {
    if (window._currentHtml) { var w = window.open('', '_blank'); w.document.write(window._currentHtml); w.document.close(); }
}
function closeFileViewer() {
    document.getElementById('fv-overlay').classList.remove('open');
    document.getElementById('fv-content').innerHTML = '';
}
function escHtml(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function showUploadModal()  { document.getElementById('uploadModal').classList.add('open'); document.getElementById('uploadStatus').innerHTML = ''; }
function closeUploadModal() { document.getElementById('uploadModal').classList.remove('open'); document.getElementById('fileInput').value = ''; }

function uploadFiles() {
    var files = document.getElementById('fileInput').files;
    if (!files.length) { document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--red)">Select at least one file</span>'; return; }
    var fd = new FormData();
    for (var i = 0; i < files.length; i++) fd.append('file', files[i]);
    fd.append('path', currentPath);
    document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--teal)"><i class="fas fa-spinner fa-spin"></i> Uploading…</span>';
    fetch('/' + ATOM_USERNAME + '/api/upload', { method: 'POST', body: fd })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.status === 'success') {
                document.getElementById('uploadStatus').innerHTML = '<span style="color:#4ade80"><i class="fas fa-check"></i> Done!</span>';
                setTimeout(function () { location.reload(); }, 1100);
            } else {
                document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--red)">Error: ' + (data.error || 'Unknown') + '</span>';
            }
        })
        .catch(function (err) { document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--red)">' + err.message + '</span>'; });
}

function showNewFolderModal()  { document.getElementById('newFolderModal').classList.add('open'); document.getElementById('folderNameInput').value = ''; }
function closeNewFolderModal() { document.getElementById('newFolderModal').classList.remove('open'); }

function createFolder() {
    var name = document.getElementById('folderNameInput').value.trim();
    if (!name) { alert('Please enter a folder name'); return; }
    var fd = new FormData();
    fd.append('path', currentPath);
    fd.append('folder', JSON.stringify({ name: name }));
    fetch('/' + ATOM_USERNAME + '/api/upload', { method: 'POST', body: fd })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.status === 'success') { closeNewFolderModal(); location.reload(); }
            else { alert('Failed: ' + (data.error || 'Unknown error')); }
        })
        .catch(function (err) { alert('Error: ' + err.message); });
}

document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeFileViewer(); closeUploadModal(); closeNewFolderModal(); }
});