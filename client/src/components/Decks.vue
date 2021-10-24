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
                    <b-form-group>
                        <b-form-radio-group
                            v-model="selectedCardType"
                            :options="['Black', 'White']"
                            buttons
                        />
                    </b-form-group>
                    <b-form-group>
                        <b-button
                            v-if="selectedCardText[0] === '_____'"
                            @click="selectedCardText.unshift('')"
                        >
                            Add Text
                        </b-button>
                        <b-button
                            v-else
                            @click="selectedCardText.unshift('_____')"
                        >
                            Add Blank
                        </b-button>
                        <div
                            v-for="(el, ind) in selectedCardText"
                            :key="`cardElement${ind}`"
                        >
                            <span
                                v-if="el === '_____'"
                            >
                                {{ el }}
                            </span>
                            <b-form-input
                                v-else
                                v-model="selectedCardText[ind]"
                            />
                        </div>
                        <b-button
                            v-if="selectedCardText[selectedCardText.length - 1] === '_____'"
                            @click="selectedCardText.push('')"
                        >
                            Add Text
                        </b-button>
                        <b-button
                            v-else
                            @click="selectedCardText.push('_____')"
                        >
                            Add Blank
                        </b-button>
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
            let cardTypeOptions = [
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
                cardTypeOptions,
                selectedCardType: cardTypeOptions[0].value,
                selectedCardText: ["_____"],
            }
        },
        created() {
            this.fetchDecks()
        },
        methods: {
            fetchDecks() {
                return fetch('http://localhost:5000/decks', {
                    method: 'get',
                    headers: {
                        'content-type': 'application/json'
                    }
                }).then(res => {
                    if (!res.ok) {
                        console.error('error!!!');
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
            }
        },
        watch: {
            error(newError) {
                if (newError) {
                    this.alertCountdown = this.dismissSecs;
                }
            }
        }
    };
</script>

<style scoped>

</style>