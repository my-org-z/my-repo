// ===== Configuration =====
const BACKEND_URL = 'https://hintai-backend.onrender.com';
// const BACKEND_URL = 'http://localhost:8000';

// ===== State =====
let currentUser = null;
let currentSection = 'help-me';
let currentMethod = null;
let cameraStream = null;
let capturedImage = null;
let uploadedFile = null;
let currentChatSession = null;

// ===== DOM Elements =====
const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.section');
const methodCards = document.querySelectorAll('.method-card');
const modalOverlay = document.getElementById('modal-overlay');
const toast = document.getElementById('toast');
const chatSidebar = document.querySelector('.chat-sidebar');
const chatToggle = document.querySelector('.chat-toggle');
const chatClose = document.getElementById('chat-close');

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initMethodSelection();
    initCamera();
    initUpload();
    initActions();
    initModals();
    initAccount();
    initChatSidebar();
    loadUser();
});

// ===== Navigation =====
function initNavigation() {
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const section = item.dataset.section;
            if (section) {
                showSection(section);
            }
        });
    });
}

function showSection(sectionName) {
    // Update nav items
    navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.section === sectionName);
    });
    
    // Update sections
    sections.forEach(section => {
        section.classList.toggle('active', section.id === sectionName);
    });
    
    currentSection = sectionName;
    
    // Load section-specific data
    if (sectionName === 'account') {
        loadAccountData();
    } else if (sectionName === 'history') {
        loadHistory();
    }
    
    // Reset input methods
    resetInputMethods();
    
    // Close chat sidebar on mobile
    if (window.innerWidth < 768) {
        closeChatSidebar();
    }
}

// ===== Method Selection =====
function initMethodSelection() {
    methodCards.forEach(card => {
        card.addEventListener('click', () => {
            const method = card.dataset.method;
            selectMethod(method);
        });
    });
}

function selectMethod(method) {
    resetInputMethods();
    currentMethod = method;
    
    const panel = document.getElementById(`${method}-panel`);
    if (panel) {
        panel.classList.remove('hidden');
    }
    
    // Initialize specific method
    if (method === 'camera') {
        startCamera();
    }
}

function resetInputMethods() {
    currentMethod = null;
    
    // Hide all panels
    document.querySelectorAll('.input-panel').forEach(panel => {
        panel.classList.add('hidden');
    });
    
    // Hide response and hint panels
    document.getElementById('response-panel').classList.add('hidden');
    document.getElementById('hint-panel').classList.add('hidden');
    
    // Stop camera
    stopCamera();
    
    // Clear file upload
    document.getElementById('file-upload').value = '';
    capturedImage = null;
    uploadedFile = null;
}

// ===== Camera =====
function initCamera() {
    document.getElementById('capture-btn').addEventListener('click', capturePhoto);
    document.getElementById('retake-btn').addEventListener('click', () => {
        document.getElementById('captured-panel').classList.add('hidden');
        document.getElementById('camera-panel').classList.remove('hidden');
        startCamera();
    });
    document.getElementById('analyze-captured').addEventListener('click', analyzeCapturedImage);
    document.getElementById('cancel-camera').addEventListener('click', () => {
        stopCamera();
        resetInputMethods();
    });
}

function startCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' },
            audio: false 
        })
            .then(stream => {
                cameraStream = stream;
                const preview = document.getElementById('camera-preview');
                preview.srcObject = stream;
            })
            .catch(err => {
                showToast(`Erreur caméra: ${err.message}`, 'error');
            });
    } else {
        showToast('Caméra non supportée', 'error');
    }
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
        const preview = document.getElementById('camera-preview');
        preview.srcObject = null;
    }
}

function capturePhoto() {
    const preview = document.getElementById('camera-preview');
    const canvas = document.getElementById('camera-canvas');
    
    canvas.width = preview.videoWidth;
    canvas.height = preview.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(preview, 0, 0, canvas.width, canvas.height);
    
    capturedImage = canvas.toDataURL('image/jpeg', 0.9);
    
    // Show captured preview
    const capturedImg = document.getElementById('captured-image');
    capturedImg.src = capturedImage;
    
    document.getElementById('camera-panel').classList.add('hidden');
    document.getElementById('captured-panel').classList.remove('hidden');
    
    stopCamera();
}

function analyzeCapturedImage() {
    if (!capturedImage) return;
    
    fetch(capturedImage)
        .then(res => res.blob())
        .then(blob => {
            const file = new File([blob], 'capture.jpg', { type: 'image/jpeg' });
            analyzeImage(file);
        });
}

// ===== Upload =====
function initUpload() {
    const uploadZone = document.getElementById('upload-zone');
    const fileUpload = document.getElementById('file-upload');
    
    uploadZone.addEventListener('click', () => fileUpload.click());
    
    fileUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
    
    // Drag and drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
    
    document.getElementById('analyze-upload').addEventListener('click', () => {
        if (uploadedFile) {
            analyzeImage(uploadedFile);
        }
    });
    
    document.getElementById('cancel-upload').addEventListener('click', resetInputMethods);
}

function handleFileUpload(file) {
    uploadedFile = file;
    
    const previewImg = document.getElementById('preview-image');
    const previewFilename = document.getElementById('preview-filename');
    const previewSize = document.getElementById('preview-size');
    
    if (file.type.startsWith('image/')) {
        previewImg.src = URL.createObjectURL(file);
        previewImg.style.display = 'block';
    } else {
        previewImg.src = '';
        previewImg.style.display = 'none';
    }
    
    previewFilename.textContent = file.name;
    previewSize.textContent = formatFileSize(file.size);
    
    document.getElementById('upload-panel').classList.add('hidden');
    document.getElementById('preview-panel').classList.remove('hidden');
}

function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} octets`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} Ko`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`;
}

// ===== Image Analysis =====
function analyzeImage(file) {
    showLoading(true);
    
    // First, analyze locally with OpenCV.js
    analyzeImageQuality(file, (quality) => {
        if (!quality.isGood) {
            showLoading(false);
            showToast(`Image de mauvaise qualité: ${quality.reason}`, 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('user_id', currentUser?.id || 'guest');
        formData.append('file', file);
        
        const endpoint = file.type === 'application/pdf' ? '/help-me/pdf' : '/help-me/image';
        
        fetch(BACKEND_URL + endpoint, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            showLoading(false);
            if (data.error) {
                showToast(data.error, 'error');
                return;
            }
            
            showResponse(data.response, data.text);
            updateCredits(data.credits);
            
            // Show hint options
            document.getElementById('hint-panel').classList.remove('hidden');
        })
        .catch(error => {
            showLoading(false);
            showToast(`Erreur: ${error.message}`, 'error');
        });
    });
}

// ===== Text Analysis =====
function analyzeText() {
    const text = document.getElementById('exercise-text').value.trim();
    if (!text) {
        showToast('Veuillez saisir un exercice', 'error');
        return;
    }
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('user_id', currentUser?.id || 'guest');
    formData.append('exercise', text);
    
    fetch(BACKEND_URL + '/help-me/text', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        showResponse(data.response);
        updateCredits(data.credits);
        
        // Show hint options
        document.getElementById('hint-panel').classList.remove('hidden');
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

// ===== Response Handling =====
function showResponse(response, extractedText = '') {
    const responsePanel = document.getElementById('response-panel');
    const streamingResponse = document.getElementById('streaming-response');
    
    // Format response with markdown-like formatting
    const formattedResponse = formatResponse(response);
    streamingResponse.innerHTML = formattedResponse;
    responsePanel.classList.remove('hidden');
    
    // Auto-scroll to response
    responsePanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function formatResponse(text) {
    // Basic markdown formatting
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n\n/g, '<p></p>')
        .replace(/\n/g, '<br>')
        .replace(/^# (.*$)/gm, '<h4>$1</h4>')
        .replace(/^- (.*$)/gm, '<li>$1</li>')
        .replace(/^\d+\. (.*$)/gm, '<li>$1</li>');
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    loading.classList.toggle('hidden', !show);
}

// ===== Hint Actions =====
function initActions() {
    // Text input
    document.getElementById('submit-text').addEventListener('click', analyzeText);
    document.getElementById('cancel-text').addEventListener('click', resetInputMethods);
    
    // Hint buttons
    document.getElementById('get-hint-1').addEventListener('click', () => getHint(1));
    document.getElementById('get-hint-2').addEventListener('click', () => getHint(2));
    document.getElementById('get-hint-3').addEventListener('click', () => getHint(3));
    document.getElementById('get-full-solution').addEventListener('click', getFullSolution);
    
    // Copy response
    document.getElementById('copy-response').addEventListener('click', () => {
        const response = document.getElementById('streaming-response').textContent;
        navigator.clipboard.writeText(response);
        showToast('Réponse copiée!', 'success');
    });
    
    // Learn concept
    document.getElementById('start-learning').addEventListener('click', startLearningConcept);
    document.getElementById('send-learning').addEventListener('click', sendLearningMessage);
    document.getElementById('end-learning').addEventListener('click', endLearningSession);
    
    // User button
    document.getElementById('user-btn').addEventListener('click', () => {
        if (currentUser) {
            showSection('account');
        } else {
            openModal('login-modal');
        }
    });
    
    // Filters
    document.getElementById('history-filter').addEventListener('change', loadHistory);
}

function getHint(number) {
    const exercise = document.getElementById('exercise-text').value.trim();
    if (!exercise) {
        showToast('Veuillez d\'abord analyser un exercice', 'error');
        return;
    }
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('user_id', currentUser?.id || 'guest');
    formData.append('exercise', exercise);
    formData.append('hint_number', number);
    
    fetch(BACKEND_URL + '/help-me/hint', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        showResponse(data.response);
        updateCredits(data.credits);
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

function getFullSolution() {
    const exercise = document.getElementById('exercise-text').value.trim();
    if (!exercise) {
        showToast('Veuillez d\'abord analyser un exercice', 'error');
        return;
    }
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('user_id', currentUser?.id || 'guest');
    formData.append('exercise', exercise);
    
    fetch(BACKEND_URL + '/help-me/full-solution', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        showResponse(data.response);
        updateCredits(data.credits);
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

// ===== Learn a Concept =====
function startLearningConcept() {
    const concept = document.getElementById('concept-input').value.trim();
    if (!concept) {
        showToast('Veuillez saisir un concept', 'error');
        return;
    }
    
    const userExplanation = document.getElementById('user-explanation').value.trim();
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('user_id', currentUser?.id || 'guest');
    formData.append('concept', concept);
    if (userExplanation) {
        formData.append('user_explanation', userExplanation);
    }
    
    fetch(BACKEND_URL + '/learn-concept', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        currentChatSession = {
            concept,
            messages: [
                { role: 'ai', content: data.response }
            ]
        };
        
        document.getElementById('concept-form').classList.add('hidden');
        document.getElementById('learning-session').classList.remove('hidden');
        document.getElementById('session-concept').textContent = concept;
        
        addLearningMessage('ai', data.response);
        updateCredits(data.credits);
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

function sendLearningMessage() {
    const input = document.getElementById('learning-input');
    const message = input.value.trim();
    if (!message) return;
    
    input.value = '';
    
    addLearningMessage('user', message);
    
    const previousResponse = currentChatSession.messages[currentChatSession.messages.length - 1].content;
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('user_id', currentUser?.id || 'guest');
    formData.append('concept', currentChatSession.concept);
    formData.append('previous_response', previousResponse);
    formData.append('user_input', message);
    
    fetch(BACKEND_URL + '/learn-concept/continue', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        addLearningMessage('ai', data.response);
        currentChatSession.messages.push({ role: 'ai', content: data.response });
        updateCredits(data.credits);
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

function addLearningMessage(role, content) {
    const messagesContainer = document.getElementById('learning-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    messageDiv.innerHTML = formatResponse(content);
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function endLearningSession() {
    currentChatSession = null;
    document.getElementById('learning-session').classList.add('hidden');
    document.getElementById('learn').querySelector('.learn-form').classList.remove('hidden');
    document.getElementById('learning-messages').innerHTML = '';
    document.getElementById('concept-input').value = '';
    document.getElementById('user-explanation').value = '';
}

// ===== Chat Sidebar =====
function initChatSidebar() {
    chatToggle.addEventListener('click', toggleChatSidebar);
    chatClose.addEventListener('click', closeChatSidebar);
    
    document.getElementById('send-ai-chat').addEventListener('click', sendAIChatMessage);
    document.getElementById('ai-chat-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendAIChatMessage();
        }
    });
}

function toggleChatSidebar() {
    chatSidebar.classList.toggle('active');
}

function closeChatSidebar() {
    chatSidebar.classList.remove('active');
}

function sendAIChatMessage() {
    const input = document.getElementById('ai-chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    input.value = '';
    
    // Add user message
    const messagesContainer = document.getElementById('ai-chat-messages');
    const userMessage = document.createElement('div');
    userMessage.className = 'chat-message user';
    userMessage.textContent = message;
    messagesContainer.appendChild(userMessage);
    
    // Remove welcome message if exists
    const welcomeMessage = messagesContainer.querySelector('.chat-welcome');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    // Show loading
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'chat-message ai';
    loadingDiv.id = 'ai-loading';
    loadingDiv.innerHTML = '<div class="spinner" style="width: 16px; height: 16px; margin: 0 auto;"></div>';
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Send to backend
    showLoading(true);
    
    const formData = new FormData();
    formData.append('user_id', currentUser?.id || 'guest');
    formData.append('exercise', message);
    
    fetch(BACKEND_URL + '/help-me/text', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        loadingDiv.remove();
        
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        // Add AI response
        const aiMessage = document.createElement('div');
        aiMessage.className = 'chat-message ai';
        aiMessage.innerHTML = formatResponse(data.response);
        messagesContainer.appendChild(aiMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        updateCredits(data.credits);
    })
    .catch(error => {
        showLoading(false);
        loadingDiv.remove();
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

// ===== Account =====
function initAccount() {
    document.getElementById('login-form').addEventListener('submit', (e) => {
        e.preventDefault();
        login();
    });
    
    document.getElementById('register-form').addEventListener('submit', (e) => {
        e.preventDefault();
        register();
    });
    
    document.getElementById('show-register').addEventListener('click', (e) => {
        e.preventDefault();
        closeModal('login-modal');
        openModal('register-modal');
    });
    
    document.getElementById('show-login').addEventListener('click', (e) => {
        e.preventDefault();
        closeModal('register-modal');
        openModal('login-modal');
    });
}

function loadUser() {
    const user = localStorage.getItem('hintai_user');
    if (user) {
        currentUser = JSON.parse(user);
        updateUserInfo();
    }
}

function updateUserInfo() {
    if (currentUser) {
        document.getElementById('credits').textContent = currentUser.credits || 20;
        document.getElementById('account-username').textContent = currentUser.username || 'Utilisateur';
        document.getElementById('account-email').textContent = currentUser.email || 'Non renseigné';
        document.getElementById('account-phone').textContent = currentUser.phone || 'Non renseigné';
        document.getElementById('account-credits').textContent = currentUser.credits || 20;
        document.getElementById('account-subscription').textContent = currentUser.subscription || 'Free';
        
        // Update progress bar
        const progress = Math.min((currentUser.credits || 20) / 20 * 100, 100);
        document.getElementById('credits-progress').style.width = `${progress}%`;
    } else {
        document.getElementById('credits').textContent = '20';
        document.getElementById('account-username').textContent = 'Invité';
        document.getElementById('account-email').textContent = 'Non renseigné';
        document.getElementById('account-phone').textContent = 'Non renseigné';
        document.getElementById('account-credits').textContent = '20';
        document.getElementById('account-subscription').textContent = 'Free';
        document.getElementById('credits-progress').style.width = '100%';
    }
}

function updateCredits(credits) {
    if (currentUser) {
        currentUser.credits = credits;
        localStorage.setItem('hintai_user', JSON.stringify(currentUser));
    }
    updateUserInfo();
}

function login() {
    const identifier = document.getElementById('login-identifier').value.trim();
    const password = document.getElementById('login-password').value;
    
    if (!identifier) {
        showToast('Veuillez saisir un identifiant', 'error');
        return;
    }
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('identifier', identifier);
    if (password) {
        formData.append('password', password);
    }
    
    fetch(BACKEND_URL + '/auth/login', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        currentUser = data.user;
        currentUser.access_token = data.access_token;
        localStorage.setItem('hintai_user', JSON.stringify(currentUser));
        
        closeModal('login-modal');
        updateUserInfo();
        showToast(`Bienvenue, ${currentUser.username}!`, 'success');
        
        if (currentSection === 'account') {
            loadAccountData();
        }
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

function register() {
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const phone = document.getElementById('register-phone').value.trim();
    const password = document.getElementById('register-password').value;
    
    if (!username) {
        showToast('Veuillez saisir un nom d\'utilisateur', 'error');
        return;
    }
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('username', username);
    if (email) formData.append('email', email);
    if (phone) formData.append('phone', phone);
    if (password) formData.append('password', password);
    
    fetch(BACKEND_URL + '/auth/register', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        currentUser = data.user;
        currentUser.access_token = data.access_token;
        localStorage.setItem('hintai_user', JSON.stringify(currentUser));
        
        closeModal('register-modal');
        updateUserInfo();
        showToast(`Compte créé avec succès!`, 'success');
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

// ===== Account Data =====
function loadAccountData() {
    if (!currentUser) {
        showToast('Veuillez vous connecter', 'error');
        openModal('login-modal');
        return;
    }
    
    fetch(BACKEND_URL + `/auth/me?user_id=${currentUser.id}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('account-username').textContent = data.username || 'Non renseigné';
        document.getElementById('account-email').textContent = data.email || 'Non renseigné';
        document.getElementById('account-phone').textContent = data.phone || 'Non renseigné';
        document.getElementById('account-subscription').textContent = data.subscription || 'Free';
        document.getElementById('account-credits').textContent = data.credits || 0;
        
        const progress = Math.min((data.credits || 20) / 20 * 100, 100);
        document.getElementById('credits-progress').style.width = `${progress}%`;
    });
}

// ===== History =====
function loadHistory() {
    if (!currentUser) {
        document.getElementById('history-list').innerHTML = '<p style="text-align: center; color: var(--gray);">Veuillez vous connecter pour voir l\'historique</p>';
        return;
    }
    
    const filter = document.getElementById('history-filter').value;
    const endpoint = filter === 'all' ? `/history?user_id=${currentUser.id}` : `/history?user_id=${currentUser.id}&action=${filter}`;
    
    fetch(BACKEND_URL + endpoint)
    .then(response => response.json())
    .then(items => {
        const container = document.getElementById('history-list');
        
        if (items.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--gray);">Aucun historique pour l\'instant</p>';
            return;
        }
        
        container.innerHTML = items.map(item => `
            <div class="history-item">
                <div class="history-item-header">
                    <span class="history-item-action">${formatAction(item.action)}</span>
                    <span class="history-item-time">${new Date(item.timestamp).toLocaleString('fr-FR', { date: 'short', time: 'short' })}</span>
                </div>
                <div class="history-item-prompt">${escapeHtml(item.prompt.substring(0, 100))}${item.prompt.length > 100 ? '...' : ''}</div>
                <div class="history-item-response">${escapeHtml(item.response.substring(0, 50))}${item.response.length > 50 ? '...' : ''}</div>
            </div>
        `).join('');
    });
}

function formatAction(action) {
    const actions = {
        'help_me_text': 'Aide (Texte)',
        'help_me_image': 'Aide (Image)',
        'help_me_pdf': 'Aide (PDF)',
        'hint_1': 'Indice 1',
        'hint_2': 'Indice 2',
        'hint_3': 'Indice 3',
        'full_solution': 'Solution complète',
        'learn_concept': 'Apprentissage',
        'learn_continue': 'Suite apprentissage',
    };
    return actions[action] || action;
}

// ===== Modals =====
function initModals() {
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.closest('.modal').id));
    });
    
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeAllModals();
        }
    });
}

function openModal(modalId) {
    modalOverlay.classList.add('active');
    document.getElementById(modalId).classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
    if (document.querySelectorAll('.modal:not(.hidden)').length === 0) {
        modalOverlay.classList.remove('active');
    }
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.add('hidden');
    });
    modalOverlay.classList.remove('active');
}

// ===== Toast =====
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ===== Utility Functions =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== Window Events =====
window.addEventListener('resize', () => {
    if (window.innerWidth >= 768 && chatSidebar.classList.contains('active')) {
        // Keep sidebar open on desktop
    } else if (window.innerWidth < 768) {
        // Close sidebar on mobile when resizing
        closeChatSidebar();
    }
});

// Close chat sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    if (window.innerWidth < 768 && chatSidebar.classList.contains('active')) {
        if (!chatSidebar.contains(e.target) && !chatToggle.contains(e.target)) {
            closeChatSidebar();
        }
    }
});
