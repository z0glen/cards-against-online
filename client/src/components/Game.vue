<template>
    <div class="container" v-if="validRoom">
        <h3>Game code: {{ code }}</h3>
        <Scoreboard :items="scoreboard"/>
        <div v-if="getState() !== 'lobby' && getState() !== 'roundOver'">
            <Card
                v-bind="getCurrentBlackCard()"
                v-bind:isBlackCard=true
            >
            </Card>
            <br>
            <h3 class="text-center">{{ this.message }}</h3>
            <div v-if="getState() === 'judging'">
                <br>
                <template v-for="(cardGroups, index) in playedCards">
                    <div :class="outline" :key="index">
                        <b-card-group deck :class="{ 'p-2': outline }">
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
            </div>
            <div v-else-if="!isJudge">
                <br>
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
        </div>
        <div v-else-if="getState() === 'roundOver'">
            <h3 class="text-center">{{ this.message }}</h3>
            <div class="center-content">
                <b-button variant="success" @click="nextRound">
                    Next Round
                </b-button>
            </div>
            <br>
            <b-card-group deck>
                <Card
                    v-bind="getCurrentBlackCard()"
                    v-bind:isBlackCard=true
                ></Card>
                <Card
                    v-bind="winData['card']"
                ></Card>
            </b-card-group>
        </div>
        <div class="text-center" v-else>
            <b-button variant="success" @click="startGame">
                Start Game
            </b-button>
        </div>
        <br>
        <div class="text-center">
            <b-button v-b-modal.history-modal>See History</b-button>
        </div>
        <b-modal id="history-modal" title="Round History">
            <p class="history-modal-content">{{ this.historyContent }}</p>
        </b-modal>
        <br>
    </div>
    <div class="container text-center" v-else>
        <h5>Invalid room ID. Try making a new game or using a different code!</h5>
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
                    return "You're the Judge! Pick the winner!";
                } else if (this.getState() === 'judging') {
                    return "All cards played! " + this.currentJudge + " is the judge.";
                } else if (this.getState() === 'roundOver') {
                    return "The verdict is in! " + this.winData['player'] + " has won!";
                } else if (!this.canPlayCard && !this.isJudge) {
                    return "Waiting for other players...";
                } else if (this.isJudge) {
                    return "You're the Judge! Waiting for players...";
                } else {
                    return "Choose a card! " + this.currentJudge + " is the judge.";
                }
            },
            isJudge() {
                return this.room['players'][this.user]['is_judge'];
            },
            players() {
                let names = Object.keys(this.room['players']);
                let players = {};
                for (let n of names) {
                    players[n] = {
                        'hasPlayedCard': !!this.room['players'][n]['playedCard'],
                        'isJudge': this.room['players'][n]['is_judge'],
                        'score': this.room['players'][n]['score']
                    }
                }
                return players;
            },
            currentJudge() {
                let names = Object.keys(this.room['players']);
                for (let n of names) {
                    if (this.room['players'][n]['is_judge']) {
                        return n;
                    }
                }
                return "";
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
                return this.getCurrentBlackCard().text.length > 2 ? 'mb-3 outline' : '';
            },
            historyContent() {
                if (Object.keys(this.room['history']).length === 0) {
                    return "No history yet!"
                }
                return JSON.stringify(this.room['history'], undefined, 4);
            },
            ...mapState(['room', 'user', 'playedCards', 'winData'])
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
            nextRound() {
                this.$socket.emit('newRound', {'room': this.code});
            }
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

    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .history-modal-content {
        white-space: pre-line;
    }
</style>