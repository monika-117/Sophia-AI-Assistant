$(document).ready(function() {
	$('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });


    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
      });

      $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    $("#MicBtn").click(function() {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.playClickSound();
        eel.allCommands()();
    });

    // Send typed text to Python when Enter is pressed
    $("#chatbox").on('keypress', function (e) {
        if (e.which === 13) { // Enter key
            var text = $(this).val().trim();
            if (text.length === 0) return;
            eel.playClickSound();
            eel.processText(text)();
            $(this).val('');
        }
    });

    // Settings: load saved values
    try {
        const savedRate = localStorage.getItem('voiceRate');
        const savedVoice = localStorage.getItem('voiceSelect');
        if (savedRate) $('#voiceRate').val(savedRate);
        if (savedVoice) $('#voiceSelect').val(savedVoice);
    } catch (e) {}

    // Show "1 2 3" on startup
    try {
        $('.siri-message li:first').text('1 2 3');
        $('.siri-message').textillate('start');
    } catch (e) {}
    $('#saveSettings').on('click', function() {
        const rate = $('#voiceRate').val();
        const voice = $('#voiceSelect').val();
        try {
            localStorage.setItem('voiceRate', rate);
            localStorage.setItem('voiceSelect', voice);
        } catch (e) {}
        // notify Python side if available
        try { eel.DisplayMessage('Settings saved.')(); } catch (e) {}

        // Gemini key handling: send to Python in memory and optionally remember locally
        try {
            const key = $('#geminiKey').val().trim();
            const remember = $('#rememberGemini').is(':checked');
            if (key.length > 0) {
                try { eel.set_gemini_key(key, remember)(); } catch (e) {}
                if (remember) {
                    try { localStorage.setItem('geminiKey', key); } catch (e) {}
                } else {
                    try { localStorage.removeItem('geminiKey'); } catch (e) {}
                }
                $('#geminiKey').val('');
            }
        } catch (e) {}
    });
});