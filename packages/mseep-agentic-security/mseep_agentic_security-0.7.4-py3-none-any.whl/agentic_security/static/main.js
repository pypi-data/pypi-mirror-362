var app = new Vue({
    el: '#vue-app',
    data: {
        progressWidth: '0%',
        modelSpec: LLM_SPECS[0],
        budget: 50,
        latency: 0,
        isFocused: false, // Tracks if the textarea is focused
        showParams: false,
        showResetConfirmation: false,
        enableChartDiagram: true,
        enableLogging: false,
        enableConcurrency: false,
        optimize: false,
        enableMultiStepAttack: false,
        scanResults: [],
        mainTable: [],
        integrationVerified: false,
        scanRunning: false,
        errorMsg: '',
        maskMode: false,
        okMsg: '',
        reportImageUrl: '',
        selectedConfig: 0,
        showModules: false,
        showLogs: false,
        showConsentModal: true,
        toasts: [], // Array to store toast notifications
        toastTimeout: 3000, // Duration in milliseconds (3 seconds)
        statusDotClass: 'bg-gray-500', // Default status dot class
        statusText: 'Verified', // Default status text
        statusClass: 'bg-green-500 text-dark-bg', // Default status class
        showLLMSpec: true, // Default to showing the LLM Spec Input
        logs: [], // This will store all the logs
        maxDisplayedLogs: 50, // Maximum number of logs to display
        configs: LLM_CONFIGS,
        dataConfig: [],
    },
    created() {
        // Check if consent is already given in local storage
        const consentGiven = localStorage.getItem('consentGiven');
        if (consentGiven === 'true') {
            this.showConsentModal = false; // Don't show the modal if consent was given
        }
    },
    mounted: function () {
        console.log('Vue app mounted');
        this.adjustHeight({ target: document.getElementById('llm-spec') });
        // this.startScan();
        this.loadConfigs();

    },
    computed: {
        selectedDS: function () {
            return this.dataConfig.filter(p => p.selected).length;
        },
        displayedLogs() {
            return this.logs.slice(-this.maxDisplayedLogs).reverse();
        },
        hasImageSpec() {
            return has_image(this.modelSpec);
        },
        hasAudioSpec() {
            return has_files(this.modelSpec);
        },
        hasFileSpec() {
            return has_files(this.modelSpec) || has_image(this.modelSpec);
        },
        highlightedText() {
            // First highlight <<VAR>> pattern
            let text = this.modelSpec.replace(
                /<<([^>]+)>>/g,
                `<span class="px-2 py-0.5 rounded-full bg-dark-accent-yellow text-dark-bg font-medium">&lt;&lt;$1&gt;&gt;</span>`
            );

            // Then highlight $VARIABLE pattern
            text = text.replace(
                /(\$[A-Z_]+)/g,
                `<span class="px-2 py-0.5 rounded-full bg-yellow-100 text-dark-bg font-medium">$1</span>`
            );

            // Finally wrap everything in gray text
            return `<span class="text-gray-500">${text}</span>`;
        },
        highlightedText2() {
            // First apply the highlighting for variables
            const highlightedText = this.modelSpec.replace(
                /<<([^>]+)>>/g,
                `<span class="px-2 py-0.5 rounded-full bg-dark-accent-yellow text-dark-bg font-medium">&lt;&lt;$1&gt;&gt;</span>`
            );

            // Wrap the entire text in a span to make non-highlighted parts dim gray
            return `<span class="text-gray-500">${highlightedText}</span>`;
        }

    },
    methods: {
        showToast(message, type = 'success') {
            const id = Date.now(); // Unique ID for each toast
            this.toasts.push({ id, message, type });

            // Automatically remove toast after timeout
            setTimeout(() => {
                this.removeToast(id);
            }, this.toastTimeout);
        },

        removeToast(id) {
            this.toasts = this.toasts.filter(toast => toast.id !== id);
        },
        focusTextarea() {
            this.isFocused = true;
            // Remove 'self' assignment if not used elsewhere
            this.$nextTick(() => {
                this.$refs.textarea.focus();
                this.adjustHeight({ target: this.$refs.textarea });
            });
            // Correct the event listener to use handleOutsideClick
            document.addEventListener("mousedown", this.handleOutsideClick);
        },
        handleOutsideClick(event) {
            if (!this.$refs.textarea) {
                return
            }
            if (!this.$refs.textarea.contains(event.target)) {
                this.isFocused = false;
                document.removeEventListener("mousedown", this.handleOutsideClick);
            }
        },
        unfocusTextarea() {
            this.isFocused = false;
        },
        acceptConsent() {
            this.showConsentModal = false; // Close the modal

            try {
                localStorage.setItem('consentGiven', 'true'); // Save consent to local storage
            } catch (e) {
                this.showToast('Failed to save consent', 'error'); // Show error if saving fails
            }
        },

        saveStateToLocalStorage() {
            const state = {
                modelSpec: this.modelSpec,
                budget: this.budget,
                selectedConfig: this.selectedConfig,
                dataConfig: this.dataConfig,
                optimize: this.optimize,
                enableChartDiagram: this.enableChartDiagram,
                enableMultiStepAttack: this.enableMultiStepAttack,
            };
            localStorage.setItem('appState:v1', JSON.stringify(state));
        },
        loadStateFromLocalStorage() {
            const savedState = localStorage.getItem('appState:v1');
            console.log('Loading state from local storage:', savedState);
            if (savedState) {
                const state = JSON.parse(savedState);
                this.modelSpec = state.modelSpec;
                this.budget = state.budget;
                this.dataConfig = state.dataConfig;
                this.optimize = state.optimize;
                this.enableChartDiagram = state.enableChartDiagram;
                this.enableMultiStepAttack = state.enableMultiStepAttack;
                this.selectedConfig = state.selectedConfig;
            }
        },
        resetState() {
            localStorage.removeItem('appState:v1');
            this.modelSpec = LLM_SPECS[0];
            this.budget = 50;
            this.dataConfig.forEach(config => config.selected = false);
            this.optimize = false;
            this.enableChartDiagram = true;
            this.okMsg = '';
            this.errorMsg = '';
            this.integrationVerified = false;
            this.showResetConfirmation = false;
            this.enableMultiStepAttack = false;
            this.showToast('All settings have been reset to default', 'info');
        },
        confirmResetState() {
            this.showResetConfirmation = true;
        },

        declineConsent() {
            this.showConsentModal = false; // Close the modal
            localStorage.setItem('consentGiven', 'false'); // Save decline to local storage
            window.location.href = 'https://www.google.com'; // Redirect to Google
        },
        updateStatusDot(ok) {
            if (ok) {
                this.statusDotClass = 'bg-green-500'; // Green when expanded
            } else if (!ok) {
                this.statusDotClass = 'bg-orange-500'; // Orange if collapsed with content
            } else {
                this.statusDotClass = 'bg-gray-500'; // Gray if collapsed without content
            }
        },
        toggleLLMSpec() {
            this.showLLMSpec = !this.showLLMSpec;
        },
        adjustHeight(event) {
            const textarea = event.target;
            event.target.style.height = 'auto';
            event.target.style.height = event.target.scrollHeight + 'px';
        },
        downloadFailures() {
            window.open('/failures', '_blank');
        },
        hide() {
            this.maskMode = !this.maskMode;
        },
        verifyIntegration: async function () {
            let payload = {
                spec: this.modelSpec,
            };
            let startTime = performance.now(); // Capture start time

            try {
                const response = await fetch(`${SELF_URL}/verify`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                });

                let r = await response.json();

                let endTime = performance.now(); // Capture end time
                let latency = ((endTime - startTime) / 1000).toFixed(3); // Calculate latency in milliseconds
                this.latency = latency;

                if (!response.ok) {
                    this.updateStatusDot(false);
                    this.errorMsg = 'Integration verification failed:' + JSON.stringify(r);
                    this.showToast('Integration verification failed', 'error');
                } else {
                    this.errorMsg = '';
                    this.updateStatusDot(true);
                    this.okMsg = 'Integration verified';
                    this.showToast('Integration verified successfully', 'success');
                    this.integrationVerified = true;
                }
            } catch (error) {
                this.updateStatusDot(true);
                this.errorMsg = 'Server unreachable';
                this.showToast('Network error', 'error');
            }

            this.saveStateToLocalStorage();
        },
        loadConfigs: async function () {
            const response = await fetch(`${SELF_URL}/v1/data-config`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            console.log(response);
            this.dataConfig = await response.json();
            this.loadStateFromLocalStorage();
        },
        selectConfig(index) {
            this.selectedConfig = index;
            this.modelSpec = LLM_SPECS[index];
            this.adjustHeight({ target: document.getElementById('llm-spec') });
            // this.adjustHeight({ target: document.getElementById('llm-spec') });
            this.errorMsg = '';
            this.okMsg = '';
            this.integrationVerified = false;
            this.showToast(`Config ${index + 1} selected`, 'info');
        },
        toggleModules() {
            this.showModules = !this.showModules;
        },
        toggleLogs() {
            this.showLogs = !this.showLogs;
        },
        addLog(message, level = 'INFO') {
            const timestamp = new Date().toISOString();
            this.logs.push({ timestamp, message, level });
        },
        downloadLogs() {
            const logText = this.logs.map(log => `${log.timestamp} [${log.level}] ${log.message}`).join('\n');
            const blob = new Blob([logText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'vulnerability_scan_logs.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },
        addPackage(index) {

            package = this.dataConfig[index];
            package.selected = !package.selected;

        },
        getFailureRateScore(failureRate) {
            return _getFailureRateScore(failureRate);
        },
        getFailureRateColor(failureRate) {
            return _getFailureRateColor(failureRate);
        },
        toggleParams() {
            this.showParams = !this.showParams;
        },
        adjustHeight(event) {
            const element = event.target;
            if (!element) {
                return
            }
            // Reset height to ensure accurate measurement
            element.style.height = 'auto';
            // Adjust height based on scrollHeight
            element.style.height = `${element.scrollHeight + 100}px`;
        },
        newEvent: function (event) {

            if (event.status) {
                this.okMsg = `${event.module}`;
                return
            }
            this.latency = event.latency.toFixed(3);
            console.log('New event');
            //  { "module": "Module 49", "tokens": 480, "cost": 4.800000000000001, "progress": 9.8 }
            let progress = event.progress;
            progress = progress % 100;
            this.progressWidth = `${progress}%`;
            this.addLog(`${JSON.stringify(event)}`, 'INFO');
            if (this.mainTable.length < 1) {
                this.mainTable.push(event);
                event.last = true;

                return
            }
            let last = this.mainTable[this.mainTable.length - 1];
            if (last.module === event.module) {
                last.tokens = event.tokens;
                last.cost = event.cost;
                last.progress = event.progress;
                last.failureRate = event.failureRate;
            } else {
                last.last = false;
                this.mainTable.push(event);
                event.last = true;
                this.newRow()
            }
            this.okMsg = `New event: ${event.module}: ${event.progress}%`;

        },
        newRow: async function () {
            if (!this.enableChartDiagram) {
                return
            }
            console.log('New row');
            this.showToast('New module', 'success');
            let payload = {
                table: this.mainTable,
            };
            const response = await fetch(`${SELF_URL}/plot.jpeg`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            // Convert image response to a data SELF_URL for the <img> src
            const blob = await response.blob();
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => {
                this.reportImageUrl = reader.result;
            };
        },
        selectAllPackages() {
            const allSelected = this.dataConfig.every(package => package.selected);

            // If all are selected, deselect all. Otherwise, select all.
            this.dataConfig.forEach(package => {
                if (!package.is_active) {
                    package.selected = false;
                    return
                }
                package.selected = !allSelected;
            });

            this.updateSelectedDS();
        },

        deselectAllPackages() {
            this.dataConfig.forEach(package => {
                package.selected = false;
            });
            this.updateSelectedDS();
        },

        updateSelectedDS() {
            this.selectedDS = this.dataConfig.filter(package => package.selected).length;
        },
        updateBudgetFromSlider(event) {
            this.budget = parseInt(event.target.value);
        },
        updateBudgetFromInput(event) {
            let value = parseInt(event.target.value);
            if (isNaN(value) || value < 1) {
                value = 1;
            } else if (value > 100) {
                value = 100;
            }
            this.budget = value;
        },
        stopScan: async function () {
            this.scanRunning = false;
            const response = await fetch(`${SELF_URL}/stop`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
        },
        startScan: async function () {
            this.showLLMSpec = false;
            let payload = {
                maxBudget: this.budget,
                llmSpec: this.modelSpec,
                datasets: this.dataConfig,
                optimize: this.optimize,
                enableMultiStepAttack: this.enableMultiStepAttack,
            };
            const response = await fetch(`${SELF_URL}/scan`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            this.okMsg = 'Scan started';
            this.mainTable = [];
            this.scanRunning = true;
            const reader = response.body.getReader();
            let receivedLength = 0; // received that many bytes at the moment
            let chunks = []; // array of received binary chunks (comprises the body)
            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    break;
                }

                chunks.push(value);
                receivedLength += value.length;

                const chunkAsString = new TextDecoder("utf-8").decode(value);
                const chunkAsLines = chunkAsString.split('\n').filter(line => line.trim());

                self = this;
                chunkAsLines.forEach(line => {
                    try {
                        const result = JSON.parse(line);
                        self.scanResults.push(result);
                        self.newEvent(result);
                    } catch (e) {
                        console.error('Error parsing chunk:', e);
                    }
                });
            }
            this.scanRunning = false;
            this.showToast('Scan finished successfully', 'success');
            this.saveStateToLocalStorage();

        }
    }
});
