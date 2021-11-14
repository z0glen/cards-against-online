<template>
    <div class="container">
        <b-alert
            :show="alertCountdown"
            variant="warning"
            dismissible
            fade
            @dismiss-count-down="countdownChanged"
        >
            {{ this.error }}
        </b-alert>
        <h1>Manage Decks</h1>
        <template v-if="!Object.keys(selectedDeck).length">
            <template v-for="(deck, name) in decks">
                <Card
                    :key="name"
                    :id="name"
                    :text="[ name ]"
                    canSelect
                    @clicked="onClick(name, deck)"
                />
            </template>
        </template>
        <div v-else>
            <h3>Deck: {{ this.selectedDeckId }}</h3>
            <b-button v-b-modal.create-card variant="primary" class="button">Create Card</b-button>
            <b-modal
                id="create-card"
                title="Create Card"
                okTitle="Create"
                @ok="handleCreateCard"
            >
                <b-form>
                    <b-form-group
                        label="Card Type"
                        description="Black cards contain blanks, white cards fill in those blanks"
                    >
                        <b-form-radio-group
                            v-model="selectedCardType"
                            :options="cardTypeOptions"
                            button-variant="outline-dark"
                            buttons
                        />
                    </b-form-group>
                    <b-form-group
                        label="Card Content"
                        :description="contentDescription"
                    >
                        <template v-if="selectedCardType">
                            <template v-if="selectedCardType === 'black'">
                                <b-button
                                    v-if="selectedCardText[0] === '_____'"
                                    size="sm"
                                    @click="selectedCardText.unshift('')"
                                >
                                    Add Text
                                </b-button>
                                <b-button
                                    v-else
                                    size="sm"
                                    @click="selectedCardText.unshift('_____')"
                                >
                                    Add Blank
                                </b-button>
                            </template>
                            <div
                                v-for="(el, ind) in selectedCardText"
                                :key="`cardElement${ind}`"
                                style="margin: 10px 0px;"
                            >
                                <span
                                    v-if="el === '_____'"
                                >
                                    __(space for white card)__
                                </span>
                                <b-form-input
                                    v-else
                                    v-model="selectedCardText[ind]"
                                    lazy-formatter
                                    :formatter="formatter"
                                />
                            </div>
                            <template v-if="selectedCardType === 'black'">
                                <b-button
                                    v-if="selectedCardText[selectedCardText.length - 1] === '_____'"
                                    size="sm"
                                    @click="selectedCardText.push('')"
                                >
                                    Add Text
                                </b-button>
                                <b-button
                                    v-else
                                    size="sm"
                                    @click="selectedCardText.push('_____')"
                                >
                                    Add Blank
                                </b-button>
                            </template>
                        </template>
                    </b-form-group>
                </b-form>
            </b-modal>
            <b-card-group
                deck
                style="margin: 25px 0px;">
                <template v-for="card in selectedDeck['calls']">
                    <Card
                        :key="`call${card.id}`"
                        v-bind="card"
                        :id="`call${card.id}`"
                        isBlackCard
                    />
                </template>
                <template v-for="card in selectedDeck['responses']">
                    <Card
                        :key="`response${card.id}`"
                        v-bind="card"
                        :id="`response${card.id}`"
                    />
                </template>
            </b-card-group>
        </div>
    </div>
</template>

<script>
    import Card from "./Card.vue";

    export default {
        components: {
            Card
        },
        data() {
            const CARD_TYPE_OPTIONS = [
                { text: "Black", value: "black" },
                { text: "White", value: "white" },
            ]
            return {
                decks: [],
                selectedDeck: {},
                selectedDeckId: "",
                error: "",
                alertCountdown: 0,
                dismissSecs: 10,
                cardTypeOptions: CARD_TYPE_OPTIONS,
                selectedCardType: null,
                selectedCardText: null,
            }
        },
        created() {
            this.fetchDecks()
        },
        computed: {
            contentDescription () {
                if (this.selectedCardType === "black") {
                    return "Black cards contain multiple parts with at least one blank. Use the 'Add Text' and 'Add Blank' buttons to add additional parts"
                } else if (this.selectedCardType === "white") {
                    return "White cards are one piece of text with no blanks";
                }
                return "Select a card type before adding content";
            }
        },
        methods: {
            fetchDecks() {
                return fetch('http://localhost:5000/decks', {
                    method: 'GET',
                    headers: {
                        'content-type': 'application/json'
                    }
                }).then(res => {
                    if (!res.ok) {
                        console.error('error fetching decks');
                        throw new Error(res.statusText);
                    }
                    return res.json();
                }).then(json => {
                    console.log(json);
                    this.decks = json;
                }).catch(err => {
                    this.error = err;
                });
            },
            countdownChanged(alertCountdown) {
                this.alertCountdown = alertCountdown;
                if (this.alertCountdown == 0) {
                    this.error = '';
                }
            },
            onClick(name, deck) {
                this.selectedDeckId = name;
                this.selectedDeck = deck;
            },
            handleCreateCard () {
                console.log(this.selectedCardText);
                return fetch('http://localhost:5000/card/create', {
                    method: 'POST',
                    headers: {
                        'content-type': 'application/json'
                    },
                    body: JSON.stringify({cardType: this.selectedCardType, cardContent: this.selectedCardText})
                }).then(res => {
                    if (!res.ok) {
                        console.error('error creating new card');
                        throw new Error(res.statusText);
                    }
                    return res.json();
                }).then(json => {
                    console.log(json);
                    this.decks = json;
                }).catch(err => {
                    this.error = err;
                });
            },
            formatter (value) {
                return value + " ";
            }
        },
        watch: {
            error(newError) {
                if (newError) {
                    this.alertCountdown = this.dismissSecs;
                }
            },
            selectedCardType (newType) {
                if (newType === 'black') {
                    this.selectedCardText = ["_____"];
                } else {
                    this.selectedCardText = [""];
                }
            }
        }
    };
</script>

<style scoped>

</style>