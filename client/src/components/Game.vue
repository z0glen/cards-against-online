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
            <div v-for="card in calls" :key="card.id">
                <Card v-bind="card">
                </Card>
            </div>
            <br>
        </div>
    </div>
</template>

<script>
    import Nav from "./Nav";
    import Card from "./Card";
    import axios from "axios";

    export default {
        components: {
            Nav,
            Card,
        },
        data() {
            return {
                loading: true,
                calls: [],
                responses: [],
            }
        },
        methods: {
            getCards() {
                const path = 'http://localhost:5000/cards';
                axios.get(path)
                    .then((res) => {
                        this.calls = res.data.calls;
                        this.responses = res.data.responses;
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