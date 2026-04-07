/**
 * Yojana Mitra — Frontend Application
 * Chat interface, form handling, and results rendering
 */

(function () {
    'use strict';

    // ============================================================
    // State
    // ============================================================
    let currentLang = 'en';
    let currentResults = null;
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

    let resultsShown = false; // Track if results have been shown

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
            // Detect if this is a scheme-discussion question (after results are shown)
            const discussKeywords = ['tell me about', 'what is', 'how to apply', 'documents', 'eligibility',
                'explain', 'details', 'benefit', 'who can', 'kaise', 'batao', 'patra',
                'dastavez', 'labh', 'first one', 'second one', 'third one', 'mudra', 'kisan',
                'ayushman', 'sukanya', 'ujjwala', 'scholarship', 'pension', 'housing', 'loan'];
            const isDiscussion = resultsShown && discussKeywords.some(kw => message.toLowerCase().includes(kw));

            let data;

            if (isDiscussion) {
                // Use the discuss endpoint
                const response = await fetch('/api/discuss', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question: message,
                        lang: currentLang
                    })
                });
                data = await response.json();
                removeTypingIndicator();

                // Format markdown-like bold text
                let answer = (data.answer || 'Sorry, I could not find an answer.')
                    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.+?)\*/g, '<em>$1</em>')
                    .replace(/\n/g, '<br>');
                addChatMessage(answer);
            } else {
                // Use the normal chat endpoint for profiling
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        profile: chatProfile,
                        lang: currentLang
                    })
                });
                data = await response.json();
                removeTypingIndicator();

                // Update accumulated profile
                if (data.profile) {
                    chatProfile = data.profile;
                }

                if (data.type === 'question') {
                    addChatMessage(data.message.replace(/\n/g, '<br>'));
                    speakResponse(data.message);
                } else if (data.type === 'results') {
                    addChatMessage(data.message.replace(/\n/g, '<br>'));
                    resultsShown = true;

                    // Add a follow-up hint
                    setTimeout(() => {
                        const hint = currentLang === 'hi'
                            ? "💡 <em>अब आप किसी भी विशेष योजना के बारे में पूछ सकते हैं! जैसे: \"PM-KISAN के बारे में बताओ\" या \"आयुष्मान भारत के लिए कौन से दस्तावेज़ चाहिए?\"</em>"
                            : "💡 <em>You can now ask me about any specific scheme! Try: \"Tell me about PM-KISAN\" or \"What documents do I need for Ayushman Bharat?\"</em>";
                        addChatMessage(hint);
                    }, 1500);

                    if (data.results) {
                        renderResults(data.results);
                        resultsSection.classList.remove('hidden');
                        setTimeout(() => {
                            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }, 300);
                    }
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
                body: JSON.stringify({ ...profile, lang: currentLang })
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
        currentResults = data; // Store for download

        // Results header
        const header = document.createElement('div');
        header.className = 'results-header';
        header.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
                <div style="text-align: left;">
                    <h2 class="results-title">🔷 ${currentLang === 'hi' ? 'आपके लिए शीर्ष योजनाएं' : 'Top Schemes For You'}</h2>
                    <p class="results-count">${currentLang === 'hi' ? 'आप' : 'You are eligible for'} <strong>${data.totalEligible} ${currentLang === 'hi' ? 'योजनाओं के लिए पात्र हैं' : 'schemes'}</strong></p>
                </div>
                <button class="persona-btn" id="downloadSummaryBtn" style="background: var(--accent-primary); color: white; border: none;">
                    📥 ${currentLang === 'hi' ? 'रिपोर्ट डाउनलोड करें' : 'Download Summary'}
                </button>
            </div>
        `;
        resultsSection.appendChild(header);

        // Download Listener
        $('#downloadSummaryBtn').onclick = () => downloadSummary(data);

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

        // Structured Reasons HTML
        let reasonsHTML = '<div class="reasons-list">';
        scheme.reasons.forEach(r => {
            reasonsHTML += `
                <div class="reason-item ${r.matched ? 'matched' : ''}">
                    <span class="icon">${r.matched ? '✅' : '❌'}</span>
                    <span>${r.label}: ${r.value}</span>
                </div>
            `;
        });
        reasonsHTML += '</div>';

        // Document Checklist (only for top 3)
        let checklistHTML = '';
        if (scheme.documentsRequired && scheme.documentsRequired.length > 0) {
            checklistHTML = `
                <div class="doc-checklist">
                    <div class="doc-checklist-title">📋 ${currentLang === 'hi' ? 'पात्रता हेतु आपके दस्तावेज़' : 'Your Application Checklist'}</div>
                    ${scheme.documentsRequired.map(doc => `
                        <label class="doc-item">
                            <input type="checkbox"> <span>${doc}</span>
                        </label>
                    `).join('')}
                </div>
            `;
        }

        card.onclick = (e) => {
            // Don't toggle if clicking buttons
            if (e.target.closest('.scheme-action-btn') || e.target.closest('input[type="checkbox"]')) return;
            toggleSelection(scheme.id, card);
        };

        card.innerHTML = `
            <div class="comparison-checkbox-container" style="position: absolute; top: 20px; right: 20px; z-index: 5; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 11px; font-weight: 700; color: var(--accent-primary); background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 4px;">${currentLang === 'hi' ? 'तुलना करें' : 'COMPARE'}</span>
                <div class="comparison-checkbox">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                </div>
            </div>

            <div class="scheme-card-header">
                <div>
                    <div class="scheme-icon">${scheme.icon}</div>
                    <div class="scheme-name">${scheme.name}</div>
                </div>
                <div class="scheme-rank">#${rank}</div>
            </div>
            
            <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px;">
                <span class="scheme-category-tag">${scheme.category}</span>
                <span class="confidence-badge ${scheme.confidenceLabel.toLowerCase().includes('highly') || scheme.confidenceLabel.includes('अत्यधिक') ? 'highly-eligible' : 'likely-eligible'}">
                    ${scheme.confidenceLabel}
                </span>
            </div>

            <!-- Match Meter -->
            <div class="eligibility-meter-row">
                <div class="meter-circle" style="--percentage: ${scheme.matchPercentage}%" data-score="${scheme.matchPercentage}%"></div>
                <div>
                    <div style="font-size: 13px; font-weight: 700;">${currentLang === 'hi' ? 'पात्रता मिलान' : 'Eligibility Confidence'}</div>
                    <div style="font-size: 11px; color: var(--text-secondary);">${currentLang === 'hi' ? 'आपके प्रोफाइल के आधार पर' : 'Based on your profile triggers'}</div>
                </div>
            </div>

            <div class="scheme-benefit">💰 ${scheme.benefit}</div>
            
            <div style="font-size: 14px; font-weight: 700; margin-top: 16px;">💡 ${currentLang === 'hi' ? 'आप पात्र क्यों हैं' : 'Why it matches your profile'}</div>
            ${reasonsHTML}
            
            <div class="scheme-explanation">${scheme.simpleExplanation}</div>
            
            ${checklistHTML}

            <div class="scheme-action-row" style="display: flex; gap: 10px; flex-wrap: wrap;">
                <a href="${scheme.officialUrl}" target="_blank" class="scheme-link scheme-action-btn official-btn" style="text-decoration:none; display:flex; align-items:center; justify-content:center;">
                    🌐 ${currentLang === 'hi' ? 'आधिकारिक आवेदन' : 'Official Apply Link'} →
                </a>
                <button class="scheme-action-btn verify-btn" onclick="speakResponse('${scheme.simpleExplanation.replace(/'/g, "\\'")}')">
                    🔊 ${currentLang === 'hi' ? 'विवरण सुनें' : 'Read Aloud'}
                </button>
                <button class="scheme-action-btn save-scheme-btn" onclick="saveScheme(this, '${scheme.id}', \`${(scheme.name || '').replace(/`/g, "'")}\`, '${scheme.icon}', \`${(scheme.benefit || '').replace(/`/g, "'")}\`)" style="flex: 1; min-width: 150px; background: rgba(16,185,129,0.1); color: var(--accent-primary); border: 1px solid var(--accent-primary); cursor: pointer; font-weight: 600; border-radius: 8px; padding: 10px 18px; font-size: 14px;">
                    ⭐ ${currentLang === 'hi' ? 'सेव करें' : 'Save to Dashboard'}
                </button>
            </div>
        `;

        return card;
    }

    // ============================================================
    // Download Summary Logic
    // ============================================================
    function downloadSummary(data) {
        let text = `--- YOJANA MITRA REPORT ---\n`;
        text += `Date: ${new Date().toLocaleDateString()}\n`;
        text += `Total Eligible Schemes: ${data.totalEligible}\n\n`;

        data.top3.forEach((s, i) => {
            text += `${i+1}. ${s.name}\n`;
            text += `   Benefit: ${s.benefit}\n`;
            text += `   Confidence: ${s.confidenceLabel}\n`;
            text += `   Why Matched: ${s.reasons.filter(r=>r.matched).map(r=>r.label).join(', ')}\n`;
            text += `   Apply: ${s.officialUrl}\n\n`;
        });

        text += `\nREQUIRED DOCUMENTS CHECKLIST:\n`;
        data.documentsRequired.forEach(doc => {
            text += `[ ] ${doc}\n`;
        });

        text += `\nDisclaimer: Always verify on official gov.in websites. This report is for information only.`;

        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Yojana_Mitra_Report_${new Date().toISOString().split('T')[0]}.txt`;
        a.click();
    }

    // ============================================================
    // Persona Logic
    // ============================================================
    $$('.persona-btn[data-persona]').forEach(btn => {
        btn.onclick = () => {
            const persona = btn.dataset.persona;
            if (persona === 'farmer') {
                $('#formAge').value = 45;
                $('#formOccupation').value = 'farmer';
                $('#formIncome').value = 80000;
                $('#formState').value = 'uttar pradesh';
                $$('.conditions-grid input').forEach(i => i.checked = (i.value === 'farmer' || i.value === 'rural'));
            } else if (persona === 'student') {
                $('#formAge').value = 20;
                $('#formOccupation').value = 'student';
                $('#formIncome').value = 150000;
                $$('.conditions-grid input').forEach(i => i.checked = (i.value === 'student'));
            } else if (persona === 'woman_entrepreneur') {
                $('#formAge').value = 32;
                $('#formGender').value = 'female';
                $('#formOccupation').value = 'entrepreneur';
                $('#formIncome').value = 300000;
                $$('.conditions-grid input').forEach(i => i.checked = (i.value === 'business'));
            } else if (persona === 'senior') {
                $('#formAge').value = 65;
                $('#formOccupation').value = 'unemployed';
                $('#formIncome').value = 50000;
                $$('.conditions-grid input').forEach(i => i.checked = (i.value === 'senior_citizen'));
            }
            
            // Highlight form
            $('#formModeBtn').click();
            profileForm.scrollIntoView({ behavior: 'smooth' });
            
            // Pulse submit button
            $('#submitBtn').classList.add('pulse');
            setTimeout(()=> $('#submitBtn').classList.remove('pulse'), 2000);
        };
    });

    // ============================================================
    // Save Scheme to Dashboard
    // ============================================================
    window.saveScheme = async function(btn, schemeId, schemeName, schemeIcon, schemeBenefit) {
        btn.disabled = true;
        btn.textContent = '⏳ Saving...';
        try {
            const res = await fetch('/api/save-scheme', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    scheme_id: schemeId,
                    scheme_name: schemeName,
                    scheme_icon: schemeIcon,
                    scheme_benefit: schemeBenefit
                })
            });
            const data = await res.json();
            if (data.saved) {
                btn.textContent = '✅ Saved!';
                btn.style.background = 'var(--accent-primary)';
                btn.style.color = 'white';
                btn.style.border = 'none';
            } else {
                btn.textContent = '❌ Error';
            }
        } catch (e) {
            btn.textContent = '❌ Error';
        }
        setTimeout(() => { btn.disabled = false; }, 2000);
    };

    // ============================================================
    // Comparison Logic
    // ============================================================
    let selectedIds = new Set();
    const MAX_COMPARE = 3;

    window.toggleSelection = function(id, el) {
        if (selectedIds.has(id)) {
            selectedIds.delete(id);
            el.classList.remove('selected');
        } else {
            if (selectedIds.size >= MAX_COMPARE) {
                alert(currentLang === 'hi' ? `आप एक बार में केवल ${MAX_COMPARE} योजनाओं की तुलना कर सकते हैं।` : `You can compare up to ${MAX_COMPARE} schemes at once.`);
                return;
            }
            selectedIds.add(id);
            el.classList.add('selected');
        }
        updateBar();
    };

    function updateBar() {
        const bar = $('#comparisonBar');
        const count = $('#compareCount');
        const btn = $('#compareBtn');
        
        if (!bar || !count || !btn) return;

        count.textContent = selectedIds.size;
        if (selectedIds.size > 0) {
            bar.classList.add('active');
            btn.disabled = selectedIds.size < 2;
            btn.style.opacity = selectedIds.size < 2 ? '0.5' : '1';
        } else {
            bar.classList.remove('active');
        }
    }

    window.clearSelection = function() {
        selectedIds.forEach(id => {
            const el = document.querySelector(`.scheme-card.selected`); // Note: simplified for dynamic results
            if (el) el.classList.remove('selected');
        });
        // Just clear all .selected cards globally in advisor
        $$('.scheme-card.selected').forEach(el => el.classList.remove('selected'));
        selectedIds.clear();
        updateBar();
    };

    window.showComparison = async function() {
        const body = $('#comparisonBody');
        body.innerHTML = '<div style="text-align:center; padding:40px;">⏳ Loading comparison data...</div>';
        $('#comparisonModal').classList.add('active');

        try {
            const res = await fetch('/api/schemes/batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ids: Array.from(selectedIds) })
            });
            const data = await res.json();
            renderComparisonTable(data.schemes);
        } catch (e) {
            body.innerHTML = '<div style="color:red; text-align:center; padding:40px;">❌ Error loading data</div>';
        }
    };

    function renderComparisonTable(schemes) {
        const body = $('#comparisonBody');
        
        let html = `<table class="comparison-table">
            <thead>
                <tr>
                    <th class="feature-col"></th>
                    ${schemes.map(s => `
                        <th class="scheme-header">
                            <div style="font-size: 32px;">${s.icon}</div>
                            <div class="scheme-title">${currentLang === 'hi' ? (s.nameHi || s.name) : s.name}</div>
                        </th>
                    `).join('')}
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="feature-col">${currentLang === 'hi' ? 'श्रेणी' : 'Category'}</td>
                    ${schemes.map(s => `<td><span class="scheme-category-tag">${s.category}</span></td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-col">${currentLang === 'hi' ? 'प्रमुख लाभ' : 'Key Benefit'}</td>
                    ${schemes.map(s => `<td class="benefit-text">${currentLang === 'hi' ? (s.benefitHi || s.benefit) : s.benefit}</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-col">${currentLang === 'hi' ? 'आयु सीमा' : 'Age Criteria'}</td>
                    ${schemes.map(s => `<td>${s.eligibility.minAge} - ${s.eligibility.maxAge} years</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-col">${currentLang === 'hi' ? 'आय सीमा' : 'Income Limit'}</td>
                    ${schemes.map(s => `<td>${s.eligibility.maxIncome < 9999999 ? 'Up to ₹' + s.eligibility.maxIncome.toLocaleString() : (currentLang === 'hi' ? 'कोई सीमा नहीं' : 'No Limit')}</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-col">${currentLang === 'hi' ? 'आवश्यक दस्तावेज़' : 'Documents Required'}</td>
                    ${schemes.map(s => `
                        <td>
                            <ul>
                                ${(currentLang === 'hi' ? (s.documentsRequiredHi || s.documentsRequired) : s.documentsRequired).map(doc => `<li>${doc}</li>`).join('')}
                            </ul>
                        </td>
                    `).join('')}
                </tr>
                <tr>
                    <td class="feature-col"></td>
                    ${schemes.map(s => `
                        <td style="text-align:center;">
                            <a href="${s.officialUrl}" target="_blank" style="display:inline-block; background:var(--accent-primary); color:white; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:12px;">Apply Now</a>
                        </td>
                    `).join('')}
                </tr>
            </tbody>
        </table>`;
        
        body.innerHTML = html;
    }

    window.closeComparison = function() {
        $('#comparisonModal').classList.remove('active');
    };

    // Focus on chat input on load
    chatInput.focus();

})();
