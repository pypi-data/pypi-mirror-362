 // 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const inputText = document.getElementById('input-text');
    const resultContainer = document.getElementById('result-container');
    const processBtn = document.getElementById('process-btn');
    const clearBtn = document.getElementById('clear-btn');
    const copyBtn = document.getElementById('copy-btn');
    const charCount = document.getElementById('char-count');
    const processStatus = document.getElementById('process-status');
    const processTime = document.getElementById('process-time');
    const processCount = document.getElementById('process-count');
    const tradToSimpBtn = document.getElementById('trad-to-simp');
    const simpToTradBtn = document.getElementById('simp-to-trad');
    const tradToSimpLabel = tradToSimpBtn.parentElement;
    const simpToTradLabel = simpToTradBtn.parentElement;
    const functionTabs = document.getElementById('functionTabs');
    const hyphenInput = document.getElementById('hyphen');
    const isCountryAbbrCheckbox = document.getElementById('is_country_abbr');
    const regexInput = document.getElementById('regex-input');
    const replaceInput = document.getElementById('replace-input');

    // 常量定义
    const RESULT_PLACEHOLDER = '转换结果将显示在这里...';
    const STATUS_READY = '准备就绪';
    const STATUS_PROCESSING = '转换中...';
    const STATUS_SUCCESS = '转换成功';
    const STATUS_ERROR = '转换失败';

    // 转换计数器和类型
    let count = 0;
    let convertType = 't2s'; // 默认繁体转简体
    let processType = 'tc_sc'; // 默认繁简转换
    let pinyinHyphen = hyphenInput.value;
    let isCountryAbbr = isCountryAbbrCheckbox.checked;

    // 工具函数：防抖
    function debounce(func, delay) {
        let timer;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timer);
            timer = setTimeout(() => {
                func.apply(context, args);
            }, delay);
        };
    }

    // 功能函数
    function updateHyphen() {
        pinyinHyphen = hyphenInput.value;
    }

    function updateCountryAbbr() {
        isCountryAbbr = isCountryAbbrCheckbox.checked;
    }

    function handleTabChange(event) {
        const activeTab = event.target;
        const activeTabId = activeTab.id;

        switch (activeTabId) {
            case 'tab-s2t':
                processType = 'tc_sc';
                break;
            case 'tab-pinyin':
                processType = 'pinyin';
                break;
            case 'tab-abbr':
                processType = 'country_zh_abbr';
                break;
            case 'tab-regex':
                processType = 'regex';
                break;
            case 'tab-encoding':
                processType = 'encoding';
                break;
            default:
                processType = 'unknown';
        }

        console.log('当前处理类型:', processType);
    }

    function updateCharCount() {
        charCount.textContent = inputText.value.length;
    }

    function clearInput() {
        inputText.value = '';
        resultContainer.value = RESULT_PLACEHOLDER;
        updateCharCount();
        processStatus.textContent = STATUS_READY;
        processTime.textContent = '0.00s';
        inputText.focus();
    }

    function copyResult() {
        const textToCopy = resultContainer.value.trim();
        if (textToCopy && textToCopy !== RESULT_PLACEHOLDER) {
            navigator.clipboard.writeText(textToCopy)
               .then(() => {
                    const originalText = copyBtn.innerHTML;
                    copyBtn.innerHTML = '已复制';
                    copyBtn.classList.add('bg-success', 'text-white', 'border-success');

                    setTimeout(() => {
                        copyBtn.innerHTML = originalText;
                        copyBtn.classList.remove('bg-success', 'text-white', 'border-success');
                    }, 2000);
                })
               .catch(err => {
                    console.error('复制失败:', err);
                    alert('复制失败，请手动复制');
                });
        }
    }

    function handleTradToSimpChange() {
        if (tradToSimpBtn.checked) {
            convertType = 't2s';
            tradToSimpLabel.classList.add('active');
            simpToTradLabel.classList.remove('active');
            inputText.placeholder = '請輸入繁體中文...';
            if (inputText.value.trim() === '') {
                resultContainer.value = RESULT_PLACEHOLDER;
            }
        }
    }

    function handleSimpToTradChange() {
        if (simpToTradBtn.checked) {
            convertType = 's2t';
            simpToTradLabel.classList.add('active');
            tradToSimpLabel.classList.remove('active');
            inputText.placeholder = '请输入简体中文...';
            if (inputText.value.trim() === '') {
                resultContainer.value = RESULT_PLACEHOLDER;
            }
        }
    }

    function validateRegex(pattern) {
        try {
            new RegExp(pattern);
            return true;
        } catch (e) {
            return false;
        }
    }

    function handleProcessClick() {
        const text = inputText.value.trim();
        if (!text) {
            alert('请输入要转换的文字');
            return;
        }

        processStatus.textContent = STATUS_PROCESSING;
        processStatus.classList.add('text-warning');
        processStatus.classList.remove('text-muted', 'text-success', 'text-danger');
        processTime.textContent = '处理中...';
        resultContainer.value = '正在进行转换，请稍候...';

        const startTime = performance.now();

        if (processType === 'regex') {
            const regexPattern = regexInput.value;
            if (!validateRegex(regexPattern)) {
                processStatus.textContent = STATUS_ERROR;
                processStatus.classList.remove('text-warning');
                processStatus.classList.add('text-danger');
                resultContainer.value = '正则表达式格式错误';
                return;
            }

            try {
                const regex = new RegExp(regexPattern, 'g');
                const replacedText = text.replace(regex, replaceInput.value);

                const endTime = performance.now();
                const duration = ((endTime - startTime) / 1000).toFixed(2);

                resultContainer.value = replacedText;
                processStatus.textContent = STATUS_SUCCESS;
                processStatus.classList.remove('text-warning');
                processStatus.classList.add('text-success');
                processTime.textContent = `${duration}s`;
                processCount.textContent = ++count;

                resultContainer.classList.add('bg-warning-subtle');
                setTimeout(() => {
                    resultContainer.classList.remove('bg-warning-subtle');
                }, 1000);
            } catch (error) {
                console.error('正则处理出错:', error);
                resultContainer.value = `正则处理出错: ${error.message}`;
                processStatus.textContent = STATUS_ERROR;
                processStatus.classList.remove('text-warning');
                processStatus.classList.add('text-danger');
            }
        } else {
            fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    direction: convertType,
                    ptype: processType,
                    pinyinHyphen: pinyinHyphen,
                    isCountryAbbr: isCountryAbbr
                })
            })
           .then(response => {
                if (!response.ok) {
                    throw new Error(`服务器返回错误: ${response.status}`);
                }
                return response.json();
            })
           .then(data => {
                const endTime = performance.now();
                const duration = ((endTime - startTime) / 1000).toFixed(2);

                resultContainer.value = data.converted_text;
                processStatus.textContent = STATUS_SUCCESS;
                processStatus.classList.remove('text-warning');
                processStatus.classList.add('text-success');
                processTime.textContent = `${duration}s`;
                processCount.textContent = ++count;

                resultContainer.classList.add('bg-warning-subtle');
                setTimeout(() => {
                    resultContainer.classList.remove('bg-warning-subtle');
                }, 1000);
            })
           .catch(error => {
                console.error('转换出错:', error);
                resultContainer.value = `转换出错: ${error.message}`;
                processStatus.textContent = STATUS_ERROR;
                processStatus.classList.remove('text-warning');
                processStatus.classList.add('text-danger');

                // 显示更友好的错误提示
                if (error.message.includes('Failed to fetch')) {
                    alert('网络连接失败，请检查您的网络设置');
                }
            });
        }
    }

    function handlePaste() {
        setTimeout(() => {
            updateCharCount();
        }, 10);
    }

    function handleDragOver(e) {
        e.preventDefault();
        inputText.classList.add('border-dashed', 'border-primary');
    }

    function handleDragLeave() {
        inputText.classList.remove('border-dashed', 'border-primary');
    }

    function handleDrop(e) {
        e.preventDefault();
        inputText.classList.remove('border-dashed', 'border-primary');

        const data = e.dataTransfer;
        if (data.items) {
            // 处理文本数据
            if (data.items[0].kind === 'string') {
                data.items[0].getAsString(function(str) {
                    inputText.value = str;
                    updateCharCount();
                });
            }
        } else {
            // 备用方法
            inputText.value = data.getData('text/plain');
            updateCharCount();
        }
    }

    // 添加事件监听器
    hyphenInput.addEventListener('input', updateHyphen);
    isCountryAbbrCheckbox.addEventListener('change', updateCountryAbbr);
    functionTabs.addEventListener('shown.bs.tab', handleTabChange);
    inputText.addEventListener('input', debounce(updateCharCount, 300)); // 防抖处理
    clearBtn.addEventListener('click', clearInput);
    copyBtn.addEventListener('click', copyResult);
    tradToSimpBtn.addEventListener('change', handleTradToSimpChange);
    simpToTradBtn.addEventListener('change', handleSimpToTradChange);
    processBtn.addEventListener('click', handleProcessClick);
    inputText.addEventListener('paste', handlePaste);
    inputText.addEventListener('dragover', handleDragOver);
    inputText.addEventListener('dragleave', handleDragLeave);
    inputText.addEventListener('drop', handleDrop); // 恢复拖放功能

    // 页面卸载时移除事件监听器
    window.addEventListener('beforeunload', function() {
        hyphenInput.removeEventListener('input', updateHyphen);
        isCountryAbbrCheckbox.removeEventListener('change', updateCountryAbbr);
        functionTabs.removeEventListener('shown.bs.tab', handleTabChange);
        inputText.removeEventListener('input', updateCharCount);
        clearBtn.removeEventListener('click', clearInput);
        copyBtn.removeEventListener('click', copyResult);
        tradToSimpBtn.removeEventListener('change', handleTradToSimpChange);
        simpToTradBtn.removeEventListener('change', handleSimpToTradChange);
        processBtn.removeEventListener('click', handleProcessClick);
        inputText.removeEventListener('paste', handlePaste);
        inputText.removeEventListener('dragover', handleDragOver);
        inputText.removeEventListener('dragleave', handleDragLeave);
        inputText.removeEventListener('drop', handleDrop);
    });

    // 初始化
    clearInput();
});
