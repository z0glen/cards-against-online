<template>
    <div class="container">
        <Nav/>
        <br>
        <div class="text-center" v-if="loading">
            <b-spinner variant="primary" label="spinning"></b-spinner>
            <br>
            Loading game content...
        </div>
        <div v-else>
            Game Content
        </div>
    </div>
</template>

<script>
    import Nav from "./Nav";
    import axios from "axios";
    export default {
        components: {Nav},
        data() {
            return {
                loading: true,
                cards: [],
            }
        },
        methods: {
            getCards() {
                const path = 'http://localhost:5000/cards';
                axios.get(path)
                    .then((res) => {
                        this.cards = res.data.cards;
                        this.loading = false;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
        },
        created() {
            this.getCards();
        }
    }
</script>

<style scoped>

</style>