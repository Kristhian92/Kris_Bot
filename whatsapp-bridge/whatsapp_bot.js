const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const RASA_URL = 'http://localhost:5005/webhooks/rest/webhook';

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    }
});

// 1. Mostrar el QR
client.on('qr', (qr) => {
    console.log('\n======================================================');
    console.log('¡ATENCIÓN! Agarra el celular con el número 3059266473');
    console.log('Abre WhatsApp Business y ESCANEA ESTE CÓDIGO QR:');
    console.log('======================================================\n');
    qrcode.generate(qr, { small: true });
});

// 2. Confirmación de conexión
client.on('ready', () => {
    console.log('\n✅ ¡ÉXITO! El bot ahora es dueño del número 3059266473 y está escuchando a todo el público.');
});

// 3. Responder a TODO el mundo (Bot Público)
client.on('message', async (msg) => {
    // Bloqueo de seguridad: No responder a grupos ni estados
    if (msg.from === 'status@broadcast' || msg.from.includes('@g.us')) return;

    console.log(`[NUEVO MENSAJE] De: ${msg.from} | Texto: ${msg.body}`);

    try {
        // Enviar a Rasa
        const response = await axios.post(RASA_URL, {
            sender: msg.from,
            message: msg.body
        });

        // Devolver la respuesta de la IA (Groq) al usuario
        const rasaResponses = response.data;
        for (const r of rasaResponses) {
            if (r.text) {
                await client.sendMessage(msg.from, r.text);
            }
        }
    } catch (error) {
        console.error('❌ Error enviando a Rasa:', error.message);
    }
});

client.initialize();
