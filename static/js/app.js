/**
 * PolicyPilot — Frontend Application
 * Chat interface, form handling, and results rendering
 */

(function () {
    'use strict';

    // ============================================================
    // State
    // ============================================================
    let currentLang = 'en';
    let chatProfile = {};  // Accumulated profile from chat conversation
    let currentMode = 'chat'; // 'chat' or 'form'

    // ============================================================
    // DOM Elements
    // ============================================================
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    const langToggle = $('#langToggle');
    const chatModeBtn = $('#chatModeBtn');
    const formModeBtn = $('#formModeBtn');
    const chatSection = $('#chatSection');
    const formSection = $('#formSection');
    const chatMessages = $('#chatMessages');
    const chatInput = $('#chatInput');
    const chatSendBtn = $('#chatSendBtn');
    const profileForm = $('#profileForm');
    const resultsSection = $('#resultsSection');

    // ============================================================
    // Language Toggle
    // ============================================================
    langToggle.addEventListener('click', () => {
        currentLang = currentLang === 'en' ? 'hi' : 'en';
        const label = $('#langLabel');
        const altLabel = $('#langLabelAlt');

        if (currentLang === 'hi') {
            label.textContent = 'हिं';
            altLabel.textContent = 'EN';
        } else {
            label.textContent = 'EN';
            altLabel.textContent = 'हिं';
        }

        // Update all translatable elements
        $$('[data-' + currentLang + ']').forEach(el => {
            const text = el.getAttribute('data-' + currentLang);
            if (text) {
                // Use textContent for option elements, innerHTML for others
                if (el.tagName === 'OPTION') {
                    el.textContent = text;
                } else {
                    el.innerHTML = text;
                }
            }
        });

        // Update placeholders
        $$('[data-' + currentLang + '-placeholder]').forEach(el => {
            const ph = el.getAttribute('data-' + currentLang + '-placeholder');
            if (ph) el.placeholder = ph;
        });
    });

    // ============================================================
    // Mode Toggle
    // ============================================================
    chatModeBtn.addEventListener('click', () => {
        currentMode = 'chat';
        chatModeBtn.classList.add('active');
        formModeBtn.classList.remove('active');
        chatSection.classList.remove('hidden');
        formSection.classList.add('hidden');
    });

    formModeBtn.addEventListener('click', () => {
        currentMode = 'form';
        formModeBtn.classList.add('active');
        chatModeBtn.classList.remove('active');
        formSection.classList.remove('hidden');
        chatSection.classList.add('hidden');
    });

    // ============================================================
    // Chat Interface
    // ============================================================
    function addChatMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg ${isUser ? 'user-msg' : 'bot-msg'} fade-in`;

        const avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.textContent = isUser ? '👤' : '🧭';

        const content = document.createElement('div');
        content.className = 'msg-content';
        content.innerHTML = `<p>${text}</p>`;

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatMessages.appendChild(msgDiv);

        // Auto scroll
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addTypingIndicator() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-msg bot-msg fade-in';
        msgDiv.id = 'typingIndicator';

        const avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.textContent = '🧭';

        const content = document.createElement('div');
        content.className = 'msg-content typing-indicator';
        content.innerHTML = `
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        `;

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = $('#typingIndicator');
        if (indicator) indicator.remove();
    }

    async function sendChatMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Show user message
        addChatMessage(message, true);
        chatInput.value = '';
        chatInput.disabled = true;
        chatSendBtn.disabled = true;

        // Show typing
        addTypingIndicator();

        try {

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    profile: chatProfile,
                    lang: currentLang
                })
            });

            const data = await response.json();
            
            removeTypingIndicator();

            // Update accumulated profile
            if (data.profile) {
                chatProfile = data.profile;
            }

            if (data.type === 'question') {
                // Bot asks follow-up
                addChatMessage(data.message.replace(/\n/g, '<br>'));
                speakResponse(data.message);
            } else if (data.type === 'results') {
                // Show summary message
                addChatMessage(data.message.replace(/\n/g, '<br>'));

                // Render results below chat
                if (data.results) {
                    renderResults(data.results);
                    resultsSection.classList.remove('hidden');

                    // Smooth scroll to results
                    setTimeout(() => {
                        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 300);
                }
            }
        } catch (error) {
            removeTypingIndicator();
            addChatMessage('Sorry, something went wrong. Please try again. 😅');
            console.error('Chat error:', error);
        }

        chatInput.disabled = false;
        chatSendBtn.disabled = false;
        chatInput.focus();
    }

    chatSendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChatMessage();
        }
    });

    // ============================================================
    // Voice Assistant (Web Speech API)
    // ============================================================
    const voiceBtn = $('#voiceBtn');
    let recognition = null;
    let isRecording = false;

    // Check browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-IN';

        recognition.onstart = () => {
            isRecording = true;
            voiceBtn.classList.add('recording');
            voiceBtn.title = 'Listening... Click to stop';
            chatInput.placeholder = '🎤 Listening...';
        };

        recognition.onresult = (event) => {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            chatInput.value = transcript;

            // Auto-send on final result
            if (event.results[event.results.length - 1].isFinal) {
                setTimeout(() => sendChatMessage(), 300);
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech error:', event.error);
            stopRecording();
            if (event.error === 'not-allowed') {
                addChatMessage('🎤 Microphone access denied. Please allow microphone access in your browser settings.');
            } else if (event.error !== 'aborted') {
                addChatMessage('🎤 Could not recognize speech. Please try again.');
            }
        };

        recognition.onend = () => {
            stopRecording();
        };

        voiceBtn.addEventListener('click', () => {
            if (isRecording) {
                recognition.stop();
            } else {
                chatInput.value = '';
                recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-IN';
                recognition.start();
            }
        });
    } else {
        // Browser doesn't support speech recognition
        voiceBtn.style.display = 'none';
    }

    function stopRecording() {
        isRecording = false;
        voiceBtn.classList.remove('recording');
        voiceBtn.title = 'Voice Input';
        chatInput.placeholder = currentLang === 'hi' ? 'अपने बारे में बताएं...' : 'Tell me about yourself...';
    }

    // Text-to-Speech for bot responses
    function speakResponse(text) {
        if ('speechSynthesis' in window) {
            // Strip HTML tags
            const clean = text.replace(/<[^>]*>/g, '').replace(/&[^;]+;/g, ' ');
            if (clean.length > 300) return; // Don't read very long responses
            const utterance = new SpeechSynthesisUtterance(clean);
            utterance.lang = currentLang === 'hi' ? 'hi-IN' : 'en-IN';
            utterance.rate = 0.95;
            utterance.pitch = 1;
            window.speechSynthesis.speak(utterance);
        }
    }

    // ============================================================
    // Form Submission
    // ============================================================
    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const btnText = $('.btn-text');
        const btnLoader = $('.btn-loader');
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');

        // Gather conditions
        const conditions = [];
        $$('.conditions-grid input[type="checkbox"]:checked').forEach(cb => {
            conditions.push(cb.value);
        });

        const profile = {
            age: $('#formAge').value,
            gender: $('#formGender').value,
            income: $('#formIncome').value,
            state: $('#formState').value,
            category: $('#formCategory').value,
            occupation: $('#formOccupation').value,
            conditions: conditions
        };

        // Sync occupation with conditions
        const occ = profile.occupation;
        if (occ === 'farmer' && !conditions.includes('farmer')) conditions.push('farmer');
        if (occ === 'student' && !conditions.includes('student')) conditions.push('student');
        if (occ === 'artisan' && !conditions.includes('artisan')) conditions.push('artisan');
        if (occ === 'street_vendor' && !conditions.includes('street_vendor')) conditions.push('street_vendor');

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profile)
            });

            const data = await response.json();

            renderResults(data);
            resultsSection.classList.remove('hidden');

            setTimeout(() => {
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 200);
        } catch (error) {
            console.error('Form submission error:', error);
            alert('Something went wrong. Please try again.');
        }

        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    });

    // ============================================================
    // Render Results
    // ============================================================
    function renderResults(data) {
        resultsSection.innerHTML = '';

        // Results header
        const header = document.createElement('div');
        header.className = 'results-header';
        header.innerHTML = `
            <h2 class="results-title">🔷 ${currentLang === 'hi' ? 'आपके लिए शीर्ष योजनाएं' : 'Top Schemes For You'}</h2>
            <p class="results-count">${currentLang === 'hi' ? 'आप' : 'You are eligible for'} <strong>${data.totalEligible} ${currentLang === 'hi' ? 'योजनाओं के लिए पात्र हैं' : 'schemes'}</strong></p>
        `;
        resultsSection.appendChild(header);

        // Top 3 schemes
        if (data.top3 && data.top3.length > 0) {
            const topSection = document.createElement('div');
            topSection.className = 'top-schemes';

            data.top3.forEach((scheme, index) => {
                const card = createSchemeCard(scheme, index + 1);
                card.style.animationDelay = `${index * 0.15}s`;
                topSection.appendChild(card);
            });

            resultsSection.appendChild(topSection);
        } else {
            // No results
            const noRes = document.createElement('div');
            noRes.className = 'no-results';
            noRes.innerHTML = `
                <div class="no-results-icon">🔍</div>
                <div class="no-results-text">${currentLang === 'hi' ? 'कोई योजना नहीं मिली' : 'No Schemes Found'}</div>
                <div class="no-results-sub">${currentLang === 'hi' ? 'कृपया अपनी प्रोफ़ाइल जानकारी जांचें' : 'Try adjusting your profile details'}</div>
            `;
            resultsSection.appendChild(noRes);
            return;
        }

        // Other schemes
        if (data.others && data.others.length > 0) {
            const othersSection = document.createElement('div');
            othersSection.className = 'other-schemes';
            othersSection.innerHTML = `<div class="other-schemes-label">📊 ${currentLang === 'hi' ? 'अन्य पात्र योजनाएं' : 'Other Eligible Schemes'}</div>`;

            data.others.forEach(scheme => {
                const item = document.createElement('div');
                item.className = 'other-scheme-item';
                item.innerHTML = `
                    <span class="other-scheme-icon">${scheme.icon}</span>
                    <div class="other-scheme-info">
                        <div class="other-scheme-name">${scheme.shortName || scheme.name}</div>
                        <div class="other-scheme-benefit">${scheme.benefit}</div>
                    </div>
                    <a href="${scheme.officialUrl}" target="_blank" class="other-scheme-link">${currentLang === 'hi' ? 'जानें →' : 'Learn More →'}</a>
                `;
                othersSection.appendChild(item);
            });

            resultsSection.appendChild(othersSection);
        }

        // Documents required
        if (data.documentsRequired && data.documentsRequired.length > 0) {
            const docsSection = document.createElement('div');
            docsSection.className = 'docs-section';

            const docsCard = document.createElement('div');
            docsCard.className = 'docs-card glass-card';

            let docsHTML = `<div class="docs-title">🧾 ${currentLang === 'hi' ? 'आवश्यक दस्तावेज़' : 'Documents You May Need'}</div>`;
            docsHTML += '<ul class="docs-list">';
            data.documentsRequired.forEach(doc => {
                docsHTML += `<li>${doc}</li>`;
            });
            docsHTML += '</ul>';

            docsCard.innerHTML = docsHTML;
            docsSection.appendChild(docsCard);
            resultsSection.appendChild(docsSection);
        }

        // Important Notes
        const notesSection = document.createElement('div');
        notesSection.className = 'notes-section';

        const notesCard = document.createElement('div');
        notesCard.className = 'notes-card glass-card';
        notesCard.innerHTML = `
            <div class="notes-title">💡 ${currentLang === 'hi' ? 'महत्वपूर्ण जानकारी' : 'Important Notes'}</div>
            <ul class="notes-list">
                <li>${currentLang === 'hi' ? 'आवेदन करने से पहले हमेशा आधिकारिक सरकारी वेबसाइट पर योजना विवरण की पुष्टि करें' : 'Always verify scheme details on official government websites before applying'}</li>
                <li>${currentLang === 'hi' ? 'अपना आधार कार्ड अपने बैंक खाते और मोबाइल नंबर से लिंक रखें' : 'Keep your Aadhaar card linked to your bank account and mobile number for DBT'}</li>
                <li>${currentLang === 'hi' ? 'DBT (डायरेक्ट बेनिफिट ट्रांसफर) के लिए आपका बैंक खाता सक्रिय होना चाहिए' : 'Your bank account must be active and KYC-compliant to receive benefits'}</li>
                <li>${currentLang === 'hi' ? 'सबसे सटीक और अद्यतन जानकारी के लिए myScheme.gov.in पर जाएं' : 'Visit <a href="https://www.myscheme.gov.in" target="_blank" style="color: var(--accent-secondary);">myScheme.gov.in</a> for the most accurate and updated information'}</li>
                <li>${currentLang === 'hi' ? 'कई योजनाओं में सहायता के लिए अपने नजदीकी CSC (कॉमन सर्विस सेंटर) जाएं' : 'Visit your nearest CSC (Common Service Centre) for help with applications for many schemes'}</li>
            </ul>
        `;
        notesSection.appendChild(notesCard);
        resultsSection.appendChild(notesSection);
    }

    function createSchemeCard(scheme, rank) {
        const card = document.createElement('div');
        card.className = 'scheme-card';
        card.setAttribute('data-category', scheme.category);

        let stepsHTML = '';
        if (scheme.howToApply && scheme.howToApply.length > 0) {
            stepsHTML = `
                <details class="scheme-details-card scheme-steps-interactive">
                    <summary class="scheme-steps-title">📋 ${currentLang === 'hi' ? 'आवेदन कैसे करें (क्लिक करें)' : 'How to Apply (Click to expand)'}</summary>
                    <div class="details-content">
                        <ol>${scheme.howToApply.map(step => `<li>${step}</li>`).join('')}</ol>
                    </div>
                </details>
            `;
        }

        card.innerHTML = `
            <div class="scheme-card-header">
                <div>
                    <div class="scheme-icon">${scheme.icon}</div>
                    <div class="scheme-name">${scheme.name}</div>
                </div>
                <div class="scheme-rank">#${rank}</div>
            </div>
            <span class="scheme-category-tag">${scheme.category}</span>
            <div class="scheme-benefit">💰 ${scheme.benefit}</div>
            <div class="scheme-why">✅ ${currentLang === 'hi' ? 'आप पात्र क्यों हैं' : 'Why you qualify'}: ${scheme.whyQualify}</div>
            <div class="scheme-explanation">${scheme.simpleExplanation}</div>
            ${stepsHTML}
            <div class="scheme-action-row">
                <a href="${scheme.officialUrl}" target="_blank" class="scheme-link scheme-action-btn">
                    🌐 ${currentLang === 'hi' ? 'आधिकारिक वेबसाइट' : 'Apply on Official Website'} →
                </a>
            </div>
        `;

        return card;
    }

    // ============================================================
    // Focus on chat input on load
    // ============================================================
    chatInput.focus();

})();
