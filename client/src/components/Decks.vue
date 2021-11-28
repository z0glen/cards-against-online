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
            <b-button v-b-modal.create-card variant="primary" class="button" @click="isCreateCardModalOpen = true">Create Card</b-button>
            <CreateCardModal
                id="create-card"
                @refresh="handleRefresh"
                @error="handleError"
            />
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
    import CreateCardModal from "./forms/CreateCardModal.vue";

    export default {
        components: {
            Card,
            CreateCardModal
        },
        data() {
            return {
                decks: [],
                selectedDeck: {},
                selectedDeckId: "",
                error: "",
                alertCountdown: 0,
                dismissSecs: 10,
            }
        },
        created() {
            this.fetchDecks()
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
            handleRefresh(json) {
                this.decks = json;
            },
            handleError(error) {
                this.error = error;
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