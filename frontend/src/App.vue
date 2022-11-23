<script setup>
import HelloWorld from "./components/HelloWorld.vue";
import TheWelcome from "./components/TheWelcome.vue";
</script>

<script>
export default {
    data() {
        return {
            inputURL: "",
            inputQR: null,
            isEnter: false,
            qrCode: null,
            url: "",
            file: "",
        };
    },
    methods: {
        not_implemented(text) {
            alert(text);
        },
        async fetchQR(url) {
            this.qrCode = null;
            const res = await fetch(
                `http://127.0.0.1:5000/url-to-qrcode?url=${url}`,
                {
                    method: "GET",
                    // mode: 'no-cors' はエラーが出る
                }
            );
            const jsonRes = await res.json();
            this.qrCode = "data:image/png;base64," + jsonRes.qrcode;
            // const binary = jsonRes.qrcode;
            // const blob = new Blob([binary]);
            // this.qrCode = window.URL.createObjectURL(blob);
        },
        async fetchURL(qrCode) {
            const res = await fetch(
                `http://127.0.0.1:5000/qrcode-to-url?qrcode=${qrCode}`,
                {
                    method: "GET",
                }
            );
            const jsonRes = await res.json();
            this.url = jsonRes.url;
        },
        dragEnter() {
            this.isEnter = true;
        },
        dragLeave() {
            this.isEnter = false;
        },
        dropFile() {
            const reader = new FileReader();
            this.file = event.dataTransfer.files[0];
            reader.onload = (event) => {
                const img_b64 = event.currentTarget.result.split(",")[1];
                this.inputQR = event.currentTarget.result;
                this.fetchURL(img_b64);
            };
            reader.readAsDataURL(this.file);
            this.dragLeave();
        },
    },
};
</script>

<template>
    <body>
        <header class="header-logo">QR-Code Converter</header>
        <hr class="header-border" />
        <main>
            <!-- <div class="main-container">
                <div class="qrcode-converter-box">QR-Code => URL</div>
                <div class="url-converter-box">URL => QR-Code</div>
            </div> -->
            <div class="url-to-qrcode-container">
                <p class="subtitle">URL to QR-Code</p>
                <form v-on:submit.prevent>
                    <input
                        placeholder="Type your URL"
                        v-model="inputURL"
                        class="input-box"
                    />
                    <br />
                    <button @click="fetchQR(inputURL)" class="input-button">
                        Convert
                    </button>
                </form>
                <div class="qrcode-result">
                    <p v-if="!qrCode">Loading...</p>
                    <img v-else :src="qrCode" class="qrcode" />
                </div>
            </div>
            <hr class="separator" />
            <!--  -->
            <!-- QR-Code => URL -->
            <!--  -->
            <div class="qrcode-to-url-container">
                <p class="subtitle">QRCode to URL</p>
                <div
                    class="qrcode-to-url-input"
                    @dragenter="dragEnter"
                    @dragleave="dragLeave"
                    @dragover.prevent
                    @drop.prevent="dropFile"
                    :class="{ enter: isEnter }"
                >
                    <p v-if="!inputQR">Upload your QR-Code</p>
                    <img
                        v-if="inputQR"
                        :src="inputQR"
                        width="200"
                        height="200"
                    />
                </div>
                <br />
                <div class="url-result">
                    <p v-if="!url">Loading...</p>
                    <a v-else v-bind:href="url">{{ url }}</a>
                </div>
            </div>
        </main>
        <hr class="footer-border" />
        <footer>
            <a href="https:uoh-dakken.com" class="footer-link"
                >データ分析研究会</a
            >
        </footer>
    </body>
</template>

<style scoped>
header {
    line-height: 1.5;
}

.logo {
    display: block;
    margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
    header {
        display: flex;
        place-items: center;
        padding-right: calc(var(--section-gap) / 2);
    }

    .logo {
        margin: 0 2rem 0 0;
    }

    header .wrapper {
        display: flex;
        place-items: flex-start;
        flex-wrap: wrap;
    }
}
</style>
