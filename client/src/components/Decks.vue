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
            <b-button v-b-modal.create-deck variant="primary" class="button" @click="isCreateDeckModalOpen = true">Create Deck</b-button>
            <CreateDeckModal
                id="create-deck"
                @refresh="handleRefresh"
                @error="handleError"
            />
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
            <h3>Deck: {{ this.selectedDeckName }}</h3>
            <b-button v-b-modal.create-card variant="primary" class="button" @click="isCreateCardModalOpen = true">Create Card</b-button>
            <CreateCardModal
                id="create-card"
                :deckId="selectedDeck.id"
                @refresh="fetchDecks"
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
    import CreateDeckModal from "./forms/CreateDeckModal.vue";

    export default {
        components: {
            Card,
            CreateCardModal,
            CreateDeckModal
        },
        data() {
            return {
                decks: [],
                selectedDeck: {},
                selectedDeckName: "",
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
                let url = process.env.VUE_APP_SERVER_URL + '/decks';
                console.log(url);
                return fetch(url, {
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
                    this.decks = json;
                }).catch(err => {
                    console.error(err);
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
                this.selectedDeckName = name;
                this.selectedDeck = deck;
            },
            handleRefresh(json) {
                this.decks = json;
            },
            handleError(error) {
                console.error(error);
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