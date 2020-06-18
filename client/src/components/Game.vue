<template>
    <div class="container" v-if="validRoom()">
        <h3>Game code: {{ code }}</h3>
        <p>Players: {{ this.players }}</p>
        <p>Current state: {{ getState() }}</p>
        <div v-if="getState() !== 'lobby'">
            <p>Current black card:</p>
            <Card
                v-bind="getCurrentBlackCard()"
                v-bind:isBlackCard=true
            >
            </Card>
            <hr>
            <div v-if="getState() === 'judging'">
                <p>Cards for judging:</p>
                <b-card-group deck>
                    <template v-for="card in playedCards">
                        <Card
                            v-bind="card"
                            v-bind:can-select="isJudge"
                            :key="card.id"
                            @clicked="judgeCard"
                        >
                        </Card>
                    </template>
                </b-card-group>
                <hr>
            </div>
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
        </div>
        <div v-else>
            <b-button variant="success" @click="startGame">
                Start Game
            </b-button>
        </div>
        <br>
    </div>
    <div class="container text-center" v-else>
        <h5>Invalid room ID</h5>
    </div>
</template>

<script>
    import Card from "./Card";
    import { mapState } from 'vuex';

    export default {
        components: {
            Card,
        },
        props: {
            code: String
        },
        computed: {
            hasPlayedCard() {
                return !!this.room['players'][this.user]['playedCard'];
            },
            message() {
                return this.hasPlayedCard ? "Waiting for other players..." : "Choose a card!"
            },
            isJudge() {
                return this.room['players'][this.user]['is_judge'];
            },
            players() {
                let names = Object.keys(this.room['players']);
                let players = {};
                for (let n of names) {
                    console.log(this.room['players'][n]['score']);
                    players[n] = {
                        'hasPlayedCard': !!this.room['players'][n]['playedCard'],
                        'isJudge': this.room['players'][n]['is_judge'],
                        'score': this.room['players'][n]['score']
                    }
                }
                return players;
            },
            ...mapState(['room', 'user', 'playedCards'])
        },
        methods: {
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
            },
            judgeCard(cardId) {
                console.log("Judge selected card: " + cardId);
                this.$socket.emit('judgeCard', {'room': this.code, 'card': cardId});
            },
        }
    }
</script>

<style scoped>

</style>