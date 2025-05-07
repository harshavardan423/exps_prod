# Contains all your HTML templates (BASE_TEMPLATE, INDEX_TEMPLATE, FILE_EXPLORER_TEMPLATE)
# HTML Templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }} - {{ username }}'s Atom Instance</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <nav class="bg-white shadow-lg">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-between">
                <div class="flex space-x-7">
                    <div class="flex items-center py-4">
                        <span class="font-semibold text-gray-500 text-lg">{{ username }}'s Atom</span>
                    </div>
                    <div class="hidden md:flex items-center space-x-1">
                        <a href="/{{ username }}/home" class="py-4 px-2 text-gray-500 hover:text-gray-900">Home</a>
                        <a href="/{{ username }}/files" class="py-4 px-2 text-gray-500 hover:text-gray-900">Files</a>
                        <a href="/{{ username }}/behaviors" class="py-4 px-2 text-gray-500 hover:text-gray-900">Behaviors</a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold mb-6">{{ title }}</h1>
        <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
            {{ content | safe }}
        </div>
        
        {% if instance_status %}
        <div class="mt-4 p-4 rounded {% if instance_status == 'online' %}bg-green-100{% else %}bg-yellow-100{% endif %}">
            <p class="text-sm">
                Instance Status: 
                <span class="font-semibold">
                    {% if instance_status == 'online' %}
                        Online
                    {% else %}
                        Offline (showing cached data)
                    {% endif %}
                </span>
            </p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Atom Exposure Server</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-6">Active Atom Instances</h1>
        
        {% if instances %}
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {% for instance in instances %}
                    <div class="bg-white rounded-lg shadow p-6">
                        <h2 class="text-xl font-semibold mb-2">{{ instance.username }}</h2>
                        <div class="space-y-2">
                            <a href="/{{ instance.username }}/home" 
                               class="block w-full text-center bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
                                View Instance
                            </a>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="bg-white rounded-lg shadow p-6">
                <p class="text-gray-500">No active instances available.</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

FILE_EXPLORER_TEMPLATE = """
<!-- File Explorer Template with Fixed Path Navigation -->
<div class="flex flex-col h-full">
    <!-- Repository Header -->
    <div class="border-b pb-4 mb-4">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <h1 class="text-xl font-semibold">File Explorer</h1>
                <span class="px-2 py-1 text-xs border rounded-full">Public</span>
            </div>
        </div>

        <!-- Path Navigation -->
        <div class="flex items-center space-x-4 mt-4">
            <div class="flex-grow">
                <div class="bg-gray-50 rounded-md px-3 py-1 text-sm breadcrumbs">
                    <a href="/{{ username }}/files" class="text-blue-500 hover:underline">root</a>
                    {% if current_path %}
                        {% set path_parts = current_path.split('/') %}
                        {% set accumulated_path = '' %}
                        {% for part in path_parts %}
                            {% if part %}
                                {% set accumulated_path = accumulated_path + '/' + part %}
                                <span class="text-gray-500">/</span>
                                <a href="/{{ username }}/files?path={{ accumulated_path[1:] | urlencode }}" class="text-blue-500 hover:underline">{{ part }}</a>
                            {% endif %}
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- File Explorer -->
    <div class="flex-grow">
        <div class="bg-white border rounded-md">
            <div class="flex items-center justify-between px-4 py-2 bg-gray-50 border-b">
                <div class="flex items-center space-x-4">
                    <a id="downloadBtn" href="#" class="text-sm text-gray-600 hover:text-gray-800">
                        <i class="fas fa-download mr-1"></i>Clone in Atom
                    </a>
                    <button id="uploadBtn" class="text-sm text-gray-600 hover:text-gray-800">
                        <i class="fas fa-upload mr-1"></i>Upload
                    </button>
                    <button id="newFolderBtn" class="text-sm text-gray-600 hover:text-gray-800">
                        <i class="fas fa-folder-plus mr-1"></i>New Folder
                    </button>
                </div>
            </div>

            <!-- File List -->
            <div class="divide-y">
                {% if current_path != "" %}
                <div class="flex items-center px-4 py-2 hover:bg-gray-50">
                    <div class="w-1/2 flex items-center">
                        <i class="fas fa-arrow-up text-gray-500 mr-2"></i>
                        <a href="/{{ username }}/files{% if parent_path %}?path={{ parent_path | urlencode }}{% endif %}" class="text-blue-500 hover:underline">Parent Directory</a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                </div>
                {% endif %}

                {% for item in file_data.folders %}
                <div class="flex items-center px-4 py-2 hover:bg-gray-50">
                    <div class="w-1/2 flex items-center">
                        <i class="fas fa-folder text-yellow-400 mr-2"></i>
                        <a href="/{{ username }}/files?path={{ (current_path + '/' + item.name).strip('/') | urlencode }}" class="hover:underline">
                            {{ item.name }}
                        </a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                    <div class="w-1/4 text-right text-gray-500 pr-4">
                        <span class="text-sm">{{ item.modified }}</span>
                    </div>
                </div>
                {% endfor %}

                {% for item in file_data.files %}
                <div class="flex items-center px-4 py-2 hover:bg-gray-50">
                    <div class="w-1/2 flex items-center">
                        <i class="{{ item.icon }} text-gray-500 mr-2"></i>
                        <a href="#" onclick="viewFile('{{ (current_path + '/' + item.name).strip('/') }}')" class="hover:underline">
                            {{ item.name }}
                        </a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">{{ item.size }}</div>
                    <div class="w-1/4 text-right text-gray-500 pr-4">
                        <span class="text-sm">{{ item.modified }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>

<!-- File Viewer Modal with HTML View Options -->
<div id="fileViewerModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-4xl mx-auto mt-10 bg-white rounded-lg">
        <div class="p-4 border-b flex items-center justify-between">
            <div>
                <h3 id="viewerFileName" class="text-lg font-medium"></h3>
                <div class="text-sm text-gray-500">
                    <span id="fileCommitInfo">Last accessed {{ datetime.now().strftime('%Y-%m-%d') }}</span>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <a id="fileDownloadBtn" href="#" class="px-3 py-1 border rounded hover:bg-gray-50">
                    <i class="fas fa-download mr-1"></i>Download
                </a>
                <button onclick="closeFileViewer()" class="text-gray-500 hover:text-gray-700">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        <div class="p-4 max-h-[70vh] overflow-auto">
            <div id="fileContent"></div>
        </div>
    </div>
</div>

<!-- Upload Modal -->
<div id="uploadModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-lg mx-auto mt-20 bg-white rounded-lg">
        <div class="p-4 border-b flex items-center justify-between">
            <h3 class="text-lg font-medium">Upload Files</h3>
            <button onclick="closeUploadModal()" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="p-6">
            <form id="uploadForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Select Files</label>
                    <input type="file" id="fileInput" multiple 
                           class="w-full px-3 py-2 border rounded text-sm">
                </div>
                <div id="uploadStatus" class="text-sm"></div>
                <div class="flex justify-end space-x-2">
                    <button type="button" onclick="closeUploadModal()" 
                            class="px-4 py-2 border rounded hover:bg-gray-50">
                        Cancel
                    </button>
                    <button type="button" onclick="uploadFiles()" 
                            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        Upload
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- New Folder Modal -->
<div id="newFolderModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-md mx-auto mt-20 bg-white rounded-lg">
        <div class="p-4 border-b flex items-center justify-between">
            <h3 class="text-lg font-medium">Create New Folder</h3>
            <button onclick="closeNewFolderModal()" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="p-6">
            <form id="newFolderForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Folder Name</label>
                    <input type="text" id="folderNameInput" 
                           class="w-full px-3 py-2 border rounded" required>
                </div>
                <div class="flex justify-end space-x-2">
                    <button type="button" onclick="closeNewFolderModal()" 
                            class="px-4 py-2 border rounded hover:bg-gray-50">
                        Cancel
                    </button>
                    <button type="button" onclick="createFolder()" 
                            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        Create
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
function viewFile(filePath) {
    // Try to fetch from our server-side cache first
    fetch(`/{{ username }}/file-content/${filePath}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('File content not available');
            }
            return response.json();
        })
        .then(data => {
            displayFileContent(data, filePath);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load file content');
        });
}

function displayFileContent(data, filePath) {
    document.getElementById('viewerFileName').textContent = data.filename;
    const contentDiv = document.getElementById('fileContent');
    
    // Set up download button with improved handling for all file types
    const downloadBtn = document.getElementById('fileDownloadBtn');
    downloadBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        try {
            // Handle different content formats based on file type
            let binaryContent;
            
            // For text files, we might need special handling
            if (data.mime_type.startsWith('text/') || 
                data.mime_type === 'application/json' || 
                data.mime_type === 'application/javascript') {
                
                try {
                    // First try to decode as base64
                    binaryContent = atob(data.content);
                } catch (decodeError) {
                    // If not valid base64, use the content directly
                    // Convert string content to binary
                    const encoder = new TextEncoder();
                    binaryContent = String.fromCharCode(...encoder.encode(data.content));
                }
            } else {
                // For binary files, decode from base64
                binaryContent = atob(data.content);
            }
            
            // Convert to array buffer
            const bytes = new Uint8Array(binaryContent.length);
            for (let i = 0; i < binaryContent.length; i++) {
                bytes[i] = binaryContent.charCodeAt(i);
            }
            
            // Create blob and download
            const blob = new Blob([bytes], {type: data.mime_type || 'application/octet-stream'});
            const url = window.URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            
            // Clean up
            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 100);
        } catch (err) {
            console.error("Download error:", err);
            alert("There was a problem downloading the file. Please try again.");
        }
    });
    
    // Check if it's an HTML file and provide view options
    if (data.filename.endsWith('.html') || data.mime_type === 'text/html') {
        // Create toggle buttons for raw/rendered view
        const viewOptionsHtml = `
            <div class="mb-4 flex space-x-2">
                <button id="viewRawBtn" class="px-3 py-1 border rounded bg-gray-100 hover:bg-gray-200">View Raw</button>
                <button id="viewRenderedBtn" class="px-3 py-1 border rounded hover:bg-gray-100">View Rendered</button>
            </div>
            <div id="rawContentView" class="block">
                <pre class="whitespace-pre-wrap p-4 bg-gray-50 rounded border">${escapeHtml(data.content)}</pre>
            </div>
        `;
        
        contentDiv.innerHTML = viewOptionsHtml;
        
        // Add event listeners to toggle buttons
        setTimeout(() => {
            document.getElementById('viewRawBtn').addEventListener('click', function() {
                document.getElementById('rawContentView').classList.remove('hidden');
                document.getElementById('viewRawBtn').classList.add('bg-gray-100');
                document.getElementById('viewRenderedBtn').classList.remove('bg-gray-100');
            });
            
            document.getElementById('viewRenderedBtn').addEventListener('click', function() {
                // Open in new window
                const newWindow = window.open('', '_blank');
                newWindow.document.write(data.content);
                newWindow.document.close();
            });
        }, 0);
    } else if (data.mime_type.startsWith('image/')) {
        contentDiv.innerHTML = `<img src="data:${data.mime_type};base64,${data.content}" class="max-w-full">`;
    } else if (data.mime_type.startsWith('text/') || data.mime_type === 'application/json' || 
               data.mime_type === 'application/javascript') {
        contentDiv.innerHTML = `<pre class="whitespace-pre-wrap p-4 bg-gray-50 rounded border">${escapeHtml(data.content)}</pre>`;
    } else {
        contentDiv.innerHTML = `<div class="text-center">
            <p>File type: ${data.mime_type}</p>
            <p class="mt-2">Click the download button above to download this file.</p>
        </div>`;
    }
    
    document.getElementById('fileViewerModal').classList.remove('hidden');
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function closeFileViewer() {
    document.getElementById('fileViewerModal').classList.add('hidden');
    document.getElementById('fileContent').innerHTML = '';
}

// Upload functionality
function showUploadModal() {
    document.getElementById('uploadModal').classList.remove('hidden');
    document.getElementById('uploadStatus').innerHTML = '';
}

function closeUploadModal() {
    document.getElementById('uploadModal').classList.add('hidden');
    document.getElementById('fileInput').value = '';
    document.getElementById('uploadStatus').innerHTML = '';
}

function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    
    if (files.length === 0) {
        document.getElementById('uploadStatus').innerHTML = 
            '<p class="text-red-500">Please select at least one file to upload</p>';
        return;
    }
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
    }
    
    // Add current path
    formData.append('path', '{{ current_path }}');
    
    document.getElementById('uploadStatus').innerHTML = 
        '<p class="text-blue-500">Uploading files...</p>';
    
    fetch(`/{{ username }}/api/upload`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('uploadStatus').innerHTML = 
                '<p class="text-green-500">Files uploaded successfully!</p>';
            
            // Reload the page after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            document.getElementById('uploadStatus').innerHTML = 
                `<p class="text-red-500">Upload failed: ${data.error || 'Unknown error'}</p>`;
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        document.getElementById('uploadStatus').innerHTML = 
            '<p class="text-red-500">Upload failed. Please try again.</p>';
    });
}

// New folder functionality
function showNewFolderModal() {
    document.getElementById('newFolderModal').classList.remove('hidden');
    document.getElementById('folderNameInput').value = '';
}

function closeNewFolderModal() {
    document.getElementById('newFolderModal').classList.add('hidden');
}

function createFolder() {
    const folderName = document.getElementById('folderNameInput').value.trim();
    
    if (!folderName) {
        alert('Please enter a folder name');
        return;
    }
    
    const formData = new FormData();
    formData.append('path', '{{ current_path }}');
    formData.append('folder', JSON.stringify({ name: folderName }));
    
    fetch(`/{{ username }}/api/upload`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            closeNewFolderModal();
            // Reload the page to show the new folder
            window.location.reload();
        } else {
            alert(`Failed to create folder: ${data.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('Error creating folder:', error);
        alert('Failed to create folder. Please try again.');
    });
}

// Add event listeners for buttons
document.getElementById('downloadBtn').addEventListener('click', function (e) {
    e.preventDefault(); // Prevents default link behavior
    const repoName = "{{ repo_name }}";
    const downloadUrl = `/api/download?repo=${repoName}`;

    fetch(downloadUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to download repository');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${repoName}.zip`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Download error:', error);
            alert('Download failed.');
        });
});

document.getElementById('uploadBtn').addEventListener('click', showUploadModal);
document.getElementById('newFolderBtn').addEventListener('click', showNewFolderModal);
</script>
"""
