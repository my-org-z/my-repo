// ===== Configuration =====
const BACKEND_URL = 'http://localhost:8000';
// const BACKEND_URL = 'https://hintai-backend.onrender.com';

// ===== State =====
let currentUser = null;
let currentSection = 'help-me';
let currentMethod = null;
let currentSession = null;
let cameraStream = null;
let capturedImage = null;
let uploadedFile = null;

// ===== DOM Elements =====
const navBtns = document.querySelectorAll('.nav-btn');
const sections = document.querySelectorAll('.section');
const methodCards = document.querySelectorAll('.method-card');
const modalOverlay = document.getElementById('modal-overlay');
const toast = document.getElementById('toast');

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initMethodSelection();
    initCamera();
    initUpload();
    initActions();
    initModals();
    initAccount();
    loadUser();
});

// ===== Navigation =====
function initNavigation() {
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            showSection(section);
        });
    });
}

function showSection(sectionName) {
    // Update nav buttons
    navBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.section === sectionName);
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
    
    const inputPanel = document.getElementById(`${method}-input`);
    if (inputPanel) {
        inputPanel.classList.remove('hidden');
    }
    
    // Initialize specific method
    if (method === 'camera') {
        startCamera();
    }
}

function resetInputMethods() {
    currentMethod = null;
    
    // Hide all input panels
    document.querySelectorAll('.input-panel').forEach(panel => {
        panel.classList.add('hidden');
    });
    
    // Hide captured preview
    document.getElementById('captured-preview').classList.add('hidden');
    document.getElementById('upload-preview').classList.add('hidden');
    
    // Hide response
    document.getElementById('ai-response').classList.add('hidden');
    document.getElementById('hint-options').classList.add('hidden');
    
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
        document.getElementById('captured-preview').classList.add('hidden');
        startCamera();
    });
    document.getElementById('analyze-captured').addEventListener('click', () => {
        analyzeCapturedImage();
    });
    document.getElementById('cancel-camera').addEventListener('click', () => {
        stopCamera();
        resetInputMethods();
    });
}

function startCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
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
    
    document.getElementById('camera-input').classList.add('hidden');
    document.getElementById('captured-preview').classList.remove('hidden');
    
    stopCamera();
}

function analyzeCapturedImage() {
    if (!capturedImage) return;
    
    // Convert data URL to blob
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
    
    document.getElementById('cancel-upload').addEventListener('click', () => {
        resetInputMethods();
    });
}

function handleFileUpload(file) {
    uploadedFile = file;
    
    const previewImg = document.getElementById('preview-image');
    const previewFilename = document.getElementById('preview-filename');
    const previewSize = document.getElementById('preview-size');
    
    if (file.type.startsWith('image/')) {
        previewImg.src = URL.createObjectURL(file);
        previewImg.classList.remove('hidden');
    } else {
        previewImg.src = '';
        previewImg.classList.add('hidden');
    }
    
    previewFilename.textContent = file.name;
    previewSize.textContent = formatFileSize(file.size);
    
    document.getElementById('upload-zone').classList.add('hidden');
    document.getElementById('upload-preview').classList.remove('hidden');
}

function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} octets`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} Ko`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} Mo`;
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
        
        // Create FormData for upload
        const formData = new FormData();
        formData.append('user_id', currentUser?.id || 'guest');
        formData.append('file', file);
        
        // Determine endpoint based on file type
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
            
            // Show response
            showResponse(data.response, data.text);
            updateCredits(data.credits);
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
        document.getElementById('hint-options').classList.remove('hidden');
    })
    .catch(error => {
        showLoading(false);
        showToast(`Erreur: ${error.message}`, 'error');
    });
}

// ===== Response Handling =====
function showResponse(response, extractedText = '') {
    const responsePanel = document.getElementById('ai-response');
    const streamingResponse = document.getElementById('streaming-response');
    
    streamingResponse.textContent = response;
    responsePanel.classList.remove('hidden');
    
    // Auto-scroll to response
    responsePanel.scrollIntoView({ behavior: 'smooth' });
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
    
    // Copy and save response
    document.getElementById('copy-response').addEventListener('click', () => {
        const response = document.getElementById('streaming-response').textContent;
        navigator.clipboard.writeText(response);
        showToast('Réponse copiée!', 'success');
    });
    
    // Learn concept
    document.getElementById('start-learning').addEventListener('click', startLearningConcept);
    document.getElementById('send-learning').addEventListener('click', sendLearningMessage);
    document.getElementById('end-learning').addEventListener('click', endLearningSession);
    
    // Account actions - SUSPENDU
    document.getElementById('watch-ad-btn').addEventListener('click', () => {
        showToast('Fonctionnalité suspendue: les pubs récompensées ne sont pas disponibles', 'warning');
    });
    document.getElementById('buy-credits-btn').addEventListener('click', () => {
        showToast('Fonctionnalité suspendue: l\'achat de crédits n\'est pas disponible', 'warning');
    });
    
    // Filters
    document.getElementById('history-filter').addEventListener('change', loadHistory);
    document.getElementById('clear-history').addEventListener('click', clearHistory);
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
        
        // Start learning session
        currentSession = {
            concept,
            userExplanation,
            messages: [
                { role: 'ai', content: data.response }
            ]
        };
        
        // Show learning session
        document.getElementById('concept-form').classList.add('hidden');
        document.getElementById('learning-session').classList.remove('hidden');
        document.getElementById('session-concept').textContent = concept;
        
        // Add first message to chat
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
    
    // Add user message to chat
    addLearningMessage('user', message);
    
    // Get previous response
    const previousResponse = currentSession.messages[currentSession.messages.length - 1].content;
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('user_id', currentUser?.id || 'guest');
    formData.append('concept', currentSession.concept);
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
        
        // Add AI response to chat
        addLearningMessage('ai', data.response);
        
        // Update session
        currentSession.messages.push({ role: 'ai', content: data.response });
        
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
    messageDiv.textContent = content;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function endLearningSession() {
    currentSession = null;
    document.getElementById('learning-session').classList.add('hidden');
    document.getElementById('concept-form').classList.remove('hidden');
    document.getElementById('learning-messages').innerHTML = '';
    document.getElementById('concept-input').value = '';
    document.getElementById('user-explanation').value = '';
}

// ===== Account =====
function initAccount() {
    // Login/Register
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
    // Check if user is already logged in (from localStorage)
    const user = localStorage.getItem('hintai_user');
    if (user) {
        currentUser = JSON.parse(user);
        updateUserInfo();
    }
}

function updateUserInfo() {
    if (currentUser) {
        document.getElementById('username').textContent = currentUser.username || 'Utilisateur';
        document.getElementById('credits').textContent = `${currentUser.credits || 20} crédits`;
    } else {
        document.getElementById('username').textContent = 'Invité';
        document.getElementById('credits').textContent = '20 crédits';
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
        
        // Reload account data
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

function logout() {
    currentUser = null;
    localStorage.removeItem('hintai_user');
    updateUserInfo();
    showToast('Déconnecté', 'success');
}

// ===== Account Data =====
function loadAccountData() {
    if (!currentUser) {
        showToast('Veuillez vous connecter', 'error');
        openModal('login-modal');
        return;
    }
    
    // Load user info
    fetch(BACKEND_URL + `/auth/me?user_id=${currentUser.id}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('account-username').textContent = data.username || 'Non renseigné';
        document.getElementById('account-email').textContent = data.email || 'Non renseigné';
        document.getElementById('account-phone').textContent = data.phone || 'Non renseigné';
        document.getElementById('account-subscription').textContent = data.subscription || 'Free';
        document.getElementById('account-credits').textContent = data.credits || 0;
    });
    
    // Load subscription plans
    loadSubscriptionPlans();
    
    // Load payment history
    loadPaymentHistory();
}

function loadSubscriptionPlans() {
    fetch(BACKEND_URL + '/subscriptions/plans')
    .then(response => response.json())
    .then(plans => {
        const container = document.getElementById('subscription-plans');
        container.innerHTML = '';
        
        Object.entries(plans).forEach(([key, plan]) => {
            const planDiv = document.createElement('div');
            planDiv.className = `subscription-plan ${currentUser?.subscription === key ? 'active' : ''}`;
            planDiv.innerHTML = `
                <h4>${plan.name}</h4>
                <div class="price">$${plan.price}/mois</div>
                <div class="credits">${plan.credits} crédits/mois</div>
            `;
            planDiv.addEventListener('click', () => {
                if (currentUser) {
                    selectPlan(key);
                } else {
                    showToast('Veuillez vous connecter', 'error');
                }
            });
            container.appendChild(planDiv);
        });
    });
}

function selectPlan(plan) {
    // SUSPENDU: Aucun abonnement payant n'est disponible
    showToast('Seul le plan Free est disponible pour le moment', 'warning');
}

function loadPaymentHistory() {
    if (!currentUser) return;
    
    fetch(BACKEND_URL + `/payments/history?user_id=${currentUser.id}`)
    .then(response => response.json())
    .then(payments => {
        const container = document.getElementById('payment-history');
        
        if (payments.length === 0) {
            container.innerHTML = '<p>Aucun paiement pour l\'instant</p>';
            return;
        }
        
        container.innerHTML = payments.map(payment => `
            <div class="payment-item">
                <div class="payment-item-info">
                    <div>${payment.method} - ${payment.amount} ${payment.currency}</div>
                    <div class="payment-item-status ${payment.status}">${payment.status}</div>
                </div>
                <div>${new Date(payment.created_at).toLocaleDateString()}</div>
            </div>
        `).join('');
    });
}

// ===== Payment =====
function initModals() {
    // Close modals
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.closest('.modal').id));
    });
    
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeAllModals();
        }
    });
    
    // Payment form
    document.getElementById('payment-form').addEventListener('submit', (e) => {
        e.preventDefault();
        processPayment();
    });
    
    // Load credit packs
    loadCreditPacks();
    loadSubscriptionModalPlans();
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

function loadCreditPacks() {
    fetch(BACKEND_URL + '/subscriptions/packs')
    .then(response => response.json())
    .then(packs => {
        const container = document.getElementById('credit-packs');
        container.innerHTML = '';
        
        Object.entries(packs).forEach(([key, pack]) => {
            const packDiv = document.createElement('div');
            packDiv.className = 'credit-pack';
            packDiv.innerHTML = `
                <h4>${pack.name}</h4>
                <div class="amount">$${pack.price}</div>
                <div>${pack.credits} crédits</div>
            `;
            packDiv.addEventListener('click', () => {
                if (currentUser) {
                    selectCreditPack(key);
                } else {
                    showToast('Veuillez vous connecter', 'error');
                }
            });
            container.appendChild(packDiv);
        });
    });
}

function selectCreditPack(pack) {
    // SUSPENDU: Aucun pack de crédits n'est disponible
    showToast('L\'achat de crédits n\'est pas disponible pour le moment', 'warning');
}

function loadSubscriptionModalPlans() {
    fetch(BACKEND_URL + '/subscriptions/plans')
    .then(response => response.json())
    .then(plans => {
        const container = document.getElementById('subscription-modal-plans');
        container.innerHTML = '';
        
        Object.entries(plans).forEach(([key, plan]) => {
            if (key === 'free') return; // Skip free plan
            
            const planDiv = document.createElement('div');
            planDiv.className = 'subscription-plan-modal';
            planDiv.innerHTML = `
                <h4>${plan.name}</h4>
                <div class="amount">$${plan.price}/mois</div>
                <div>${plan.credits} crédits/mois</div>
            `;
            planDiv.addEventListener('click', () => {
                selectPlan(key);
                closeModal('subscribe-modal');
            });
            container.appendChild(planDiv);
        });
    });
}

function processPayment() {
    // SUSPENDU: Aucun système de paiement n'est configuré
    showToast('Les paiements ne sont pas disponibles pour le moment', 'warning');
    closeAllModals();
}

// ===== Rewarded Ads =====
function watchRewardedAd() {
    // SUSPENDU: Les pubs récompensées ne sont pas disponibles
    showToast('Fonctionnalité suspendue: les pubs récompensées ne sont pas disponibles', 'warning');
}

// ===== History =====
function loadHistory() {
    if (!currentUser) {
        document.getElementById('history-list').innerHTML = '<p>Veuillez vous connecter pour voir l\'historique</p>';
        return;
    }
    
    const filter = document.getElementById('history-filter').value;
    const endpoint = filter === 'all' ? `/history?user_id=${currentUser.id}` : `/history?user_id=${currentUser.id}&action=${filter}`;
    
    fetch(BACKEND_URL + endpoint)
    .then(response => response.json())
    .then(items => {
        const container = document.getElementById('history-list');
        
        if (items.length === 0) {
            container.innerHTML = '<p>Aucun historique pour l\'instant</p>';
            return;
        }
        
        container.innerHTML = items.map(item => `
            <div class="history-item" onclick="loadHistoryItem('${item.id}')">
                <div class="history-item-header">
                    <span class="history-item-action">${formatAction(item.action)}</span>
                    <span class="history-item-time">${new Date(item.timestamp).toLocaleString()}</span>
                </div>
                <div class="history-item-prompt">${item.prompt.substring(0, 100)}${item.prompt.length > 100 ? '...' : ''}</div>
                <div class="history-item-response">${item.response.substring(0, 50)}${item.response.length > 50 ? '...' : ''}</div>
            </div>
        `).join('');
    });
}

function formatAction(action) {
    const actions = {
        'help_me_text': 'Help Me (Texte)',
        'help_me_image': 'Help Me (Image)',
        'help_me_pdf': 'Help Me (PDF)',
        'hint_1': 'Indice 1',
        'hint_2': 'Indice 2',
        'hint_3': 'Indice 3',
        'full_solution': 'Solution complète',
        'learn_concept': 'Learn a Concept',
        'learn_continue': 'Learn (Suite)',
    };
    return actions[action] || action;
}

function clearHistory() {
    if (!currentUser) return;
    
    if (confirm('Êtes-vous sûr de vouloir effacer tout l\'historique?')) {
        // In production, add endpoint to clear history
        showToast('Historique effacé', 'success');
        loadHistory();
    }
}

// ===== Toast Notifications =====
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ===== Utility Functions =====
function loadHistoryItem(id) {
    // In production, fetch and display the full history item
    showToast('Fonctionnalité à venir', 'info');
}
