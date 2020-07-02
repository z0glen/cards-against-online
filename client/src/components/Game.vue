<template>
    <div class="container" v-if="validRoom">
        <h3>Game code: {{ code }}</h3>
        <Scoreboard :items="scoreboard"/>
        <h5>{{ this.message }}</h5>
        <p>Current state: {{ getState() }}</p>
        <hr>
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
                    <template v-for="(cardGroups, index) in playedCards">
                        <div class="mb-3" :class="outline" :key="index">
                            <b-card-group deck class="p-2">
                                <template v-for="card in cardGroups">
                                    <Card
                                        v-bind="card"
                                        v-bind:can-select="isJudge"
                                        :key="card.id"
                                        @clicked="judgeCard"
                                    >
                                    </Card>
                                </template>
                            </b-card-group>
                        </div>
                    </template>
                <hr>
            </div>
            <p>Your hand:</p>
            <b-card-group deck>
                <template v-for="card in getCurrentCards()">
                    <Card
                        v-bind="card"
                        v-bind:canSelect="canPlayCard && !isJudge"
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
    import Scoreboard from "./Scoreboard";
    import { mapState } from 'vuex';

    export default {
        components: {
            Card,
            Scoreboard,
        },
        props: {
            code: String
        },
        computed: {
            canPlayCard() {
                return this.room['players'][this.user]['canPlayCard'];
            },
            message() {
                if (this.getState() === 'judging' && this.isJudge) {
                    return "Pick the winner!";
                } else if (this.getState() === 'judging') {
                    return "Waiting for the judge...";
                } else if (!this.canPlayCard) {
                    return "Waiting for other players...";
                } else if (this.isJudge) {
                    return "It's your turn to judge!";
                } else {
                    return "Choose a card!";
                }
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
            validRoom() {
                return !!(Object.keys(this.room).length !== 0);
            },
            scoreboard() {
                let names = Object.keys(this.room['players']);
                let stats = [];
                for (let n of names) {
                    stats.push({
                        'user': n,
                        'canPlayCard': !!this.room['players'][n]['canPlayCard'],
                        'isJudge': this.room['players'][n]['is_judge'],
                        'score': this.room['players'][n]['score']
                    });
                }
                return stats;
            },
            outline() {
                return this.getCurrentBlackCard().text.length > 2 ? 'outline' : '';
            },
            ...mapState(['room', 'user', 'playedCards'])
        },
        methods: {
            getCurrentCards() {
                return this.room['players'][this.user]['cards'];
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
                if (!this.isJudge) {
                    this.$socket.emit('playCard', {'room': this.code, 'player': this.user, 'card': cardId});
                }
            },
            judgeCard(cardId) {
                console.log("Judge selected card: " + cardId);
                this.$socket.emit('judgeCard', {'room': this.code, 'card': cardId});
            },
        },
        mounted() {
            this.$nextTick(() => {
                 this.$socket.emit('joinRoom', this.code);
            });
        }
    }
</script>

<style scoped>
    .outline {
        border-radius: 5px;
        box-shadow: 0 0 0 2px lightgray;
    }
</style>