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
                <Card
                    v-bind="getCurrentBlackCard()"
                    v-bind:isBlackCard=true
                >
                </Card>
                <hr>
                <h5>{{ this.message }}</h5>
                <p>Your hand:</p>
                <b-card-group deck>
                    <template v-for="card in getCurrentCards()">
                        <Card
                            v-bind="card"
                            v-bind:canSelect="!hasPlayedCard"
                            :key="card.id"
                            @clicked="playCard"
                        >
                        </Card>
                    </template>
                </b-card-group>
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
        computed: {
            hasPlayedCard() {
                return !!this.room['players'][this.user]['playedCard'];
            },
            message() {
                return this.hasPlayedCard ? "Waiting for other players..." : "Choose a card!"
            },
            ...mapState(['room', 'user'])
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
            getPlayers() {
                console.log(this.room['players']);
                let names = Object.keys(this.room['players']);
                let players = {};
                for (let n of names) {
                    console.log(n);
                    players[n] = {'hasPlayedCard': !!this.room['players'][n]['playedCard']}
                }
                return players;
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
            },
            playCard(cardId) {
                console.log("Playing card: " + cardId);
                this.$socket.emit('playCard', {'room': this.code, 'player': this.user, 'card': cardId});
            }
        },
        created() {
            this.getCards();
        }
    }
</script>

<style scoped>

</style>