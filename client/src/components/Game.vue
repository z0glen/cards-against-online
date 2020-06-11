<template>
    <div class="container" v-if="validRoom()">
        <Nav/>
        <br>
        <h3>Game code: {{ code }}</h3>
        <p>Players: {{ getPlayers() }}</p>
        <p>Current state: {{ getState() }}</p>
        <div class="text-center" v-if="loading">
            <b-spinner variant="primary" label="spinning"></b-spinner>
            <br>
            Loading game content...
        </div>
        <div v-else>
            <div v-if="getState() !== 'lobby'">
                <p>Current black card:</p>
                <Card v-bind="getCurrentBlackCard()">
                </Card>
                <hr>
                <p>Your hand:</p>
                <div v-for="card in getCurrentCards()" :key="card.id">
                    <Card v-bind="card">
                    </Card>
                </div>
                <hr>
            </div>
            <div v-else>
                <b-button variant="success" @click="startGame">
                    Start Game
                </b-button>
            </div>
            <p>All cards:</p>
            <div v-for="card in calls" :key="card.id">
                <Card v-bind="card">
                </Card>
            </div>
            <br>
        </div>
    </div>
    <div v-else>
        <Nav />
        <span>Invalid room ID</span>
    </div>
</template>

<script>
    import Nav from "./Nav";
    import Card from "./Card";
    import axios from "axios";
    import { mapState } from 'vuex';

    export default {
        components: {
            Nav,
            Card,
        },
        props: {
            code: String
        },
        data() {
            return {
                loading: true,
                calls: [],
                responses: [],
            }
        },
        computed: mapState(['room', 'user']),
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
            getPlayers() {
                return this.room['players'];
            },
            getCurrentCards() {
                return this.room['players'][this.user]['cards'];
            },
            validRoom() {
                return Object.keys(this.room).length !== 0;
            },
            getState() {
                return this.room['state'];
            },
            startGame() {
                this.$socket.emit('setState', {'room': this.code, 'state': "active"});
            },
            getCurrentBlackCard() {
                return this.room['black_card']
            }
        },
        created() {
            this.getCards();
        }
    }
</script>

<style scoped>

</style>