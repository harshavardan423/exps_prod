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
<div class="flex flex-col h-full">
    <!-- Repository Header -->
    <div class="border-b pb-4 mb-4">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <h1 class="text-xl font-semibold">{{ repo_name }}</h1>
                <span class="px-2 py-1 text-xs border rounded-full">Public</span>
            </div>
        </div>

        <!-- Path Navigation (Removed Branch Selector) -->
        <div class="flex items-center space-x-4 mt-4">
            <div class="flex-grow">
                <div class="bg-gray-50 rounded-md px-3 py-1 text-sm">
                    <span class="text-gray-500">/</span>
                    {% for part in path_parts %}
                    <a href="/{{ username }}/files?path={{ part.path }}" class="text-blue-500 hover:underline">{{ part.name }}</a>
                    <span class="text-gray-500">/</span>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <!-- File Explorer -->
    <div class="flex-grow">
        <div class="bg-white border rounded-md">
            <div class="flex items-center justify-between px-4 py-2 bg-gray-50 border-b">
                <div class="flex items-center space-x-4">
                    <button onclick="createNewFile()" class="text-sm px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600">
                        Add file
                    </button>
                    <label for="fileUpload" class="text-sm px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 cursor-pointer">
                        Upload files
                    </label>
                    <input type="file" id="fileUpload" class="hidden" multiple>
                </div>
                <div class="flex items-center space-x-2">
                    <a id="downloadBtn" href="#" class="text-sm text-gray-600 hover:text-gray-800">
                        <i class="fas fa-download mr-1"></i>Clone in Atom
                    </a>

                </div>
            </div>

            <!-- File List -->
            <div class="divide-y">
                {% if current_path != "" %}
                <div class="flex items-center px-4 py-2 hover:bg-gray-50">
                    <div class="w-1/2 flex items-center">
                        <i class="fas fa-arrow-up text-gray-500 mr-2"></i>
                        <a href="/{{ username }}/files?path={{ parent_path }}" class="text-blue-500 hover:underline">...</a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                </div>
                {% endif %}

                {% for item in file_data.folders %}
                <div class="flex items-center px-4 py-2 hover:bg-gray-50">
                    <div class="w-1/2 flex items-center">
                        <i class="fas fa-folder text-yellow-400 mr-2"></i>
                        <a href="/{{ username }}/files?path={{ current_path_prefix }}{{ item.name }}" class="hover:underline">
                            {{ item.name }}
                        </a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                    <div class="w-1/4 text-right text-gray-500 pr-4">
                        <span class="text-sm">{{ item.modified }}</span>
                        <button class="ml-2 text-gray-400 hover:text-gray-600">
                            <i class="fas fa-ellipsis-h"></i>
                        </button>
                    </div>
                </div>
                {% endfor %}

                {% for item in file_data.files %}
                <div class="flex items-center px-4 py-2 hover:bg-gray-50">
                    <div class="w-1/2 flex items-center">
                        <i class="{{ item.icon }} text-gray-500 mr-2"></i>
                        <a href="#" onclick="viewFile('{{ current_path_prefix }}{{ item.name }}')" class="hover:underline">
                            {{ item.name }}
                        </a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">{{ item.size }}</div>
                    <div class="w-1/4 text-right text-gray-500 pr-4">
                        <span class="text-sm">{{ item.modified }}</span>
                        <button class="ml-2 text-gray-400 hover:text-gray-600">
                            <i class="fas fa-ellipsis-h"></i>
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <!-- Analytics Section -->
    <div class="mt-8 border-t pt-8">
        <h2 class="text-lg font-semibold mb-4">Files Insights</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Commit Activity Graph -->
            <div class="border rounded-lg p-4">
                <h3 class="text-sm font-medium mb-4">Commit Activity</h3>
                <div class="h-48 bg-gray-50 rounded flex items-center justify-center">
                    <!-- Placeholder for commit activity graph -->
                    <span class="text-gray-400">Commit activity visualization</span>
                </div>
            </div>

            <!-- Traffic Graph -->
            <div class="border rounded-lg p-4">
                <h3 class="text-sm font-medium mb-4">Traffic</h3>
                <div class="h-48 bg-gray-50 rounded flex items-center justify-center">
                    <!-- Placeholder for traffic graph -->
                    <span class="text-gray-400">Traffic visualization</span>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- File Viewer Modal (Removed Edit and History buttons) -->
<div id="fileViewerModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-4xl mx-auto mt-10 bg-white rounded-lg">
        <div class="p-4 border-b flex items-center justify-between">
            <div>
                <h3 id="viewerFileName" class="text-lg font-medium"></h3>
                <div class="text-sm text-gray-500">
                    <span id="fileCommitInfo">Last committed 2 days ago</span>
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

<script>
// Existing JavaScript functions...
document.getElementById('fileUpload').addEventListener('change', function(e) {
    const files = e.target.files;
    if (files.length > 0) {
        uploadFiles(files);
    }
});

function uploadFiles(files) {
    const formData = new FormData();
    formData.append('path', '{{ current_path }}');
    formData.append('branch', '{{ current_branch }}');
    
    for (let file of files) {
        formData.append('file', file);
    }

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.reload();
        } else {
            alert('Upload failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Upload failed');
    });
}

function createNewFile() {
    // Implement new file creation logic
}

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
            displayFileContent(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load file content');
        });
}

function displayFileContent(data) {
    document.getElementById('viewerFileName').textContent = data.filename;
    const contentDiv = document.getElementById('fileContent');
    
    // Set up download button
    const downloadBtn = document.getElementById('fileDownloadBtn');
    downloadBtn.href = `data:${data.mime_type};base64,${data.content}`;
    downloadBtn.setAttribute('download', data.filename);
    
    // Also set up the main download button
    const mainDownloadBtn = document.getElementById('downloadBtn');
    mainDownloadBtn.href = `data:${data.mime_type};base64,${data.content}`;
    mainDownloadBtn.setAttribute('download', data.filename);
    
    if (data.mime_type.startsWith('image/')) {
        contentDiv.innerHTML = `<img src="data:${data.mime_type};base64,${data.content}" class="max-w-full">`;
    } else if (data.mime_type.startsWith('text/') || data.mime_type === 'application/json' || 
               data.mime_type === 'application/javascript') {
        contentDiv.innerHTML = `<pre class="whitespace-pre-wrap">${escapeHtml(data.content)}</pre>`;
    } else {
        contentDiv.innerHTML = `<div class="text-center">
            <p>File type: ${data.mime_type}</p>
            <a href="data:${data.mime_type};base64,${data.content}" 
                download="${data.filename}" 
                class="bg-blue-500 text-white px-4 py-2 rounded mt-4 inline-block">
                Download File
            </a>
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


// Add any additional JavaScript functions for analytics visualization here
</script>
"""
