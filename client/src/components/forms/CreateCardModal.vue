<template>
    <b-modal
        :id="id"
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
</template>

<script>
    export default {
        props: {
            id: { type: String, required: true },
            deckId: { type: Number, required: true }
        },
        data () {
            const CARD_TYPE_OPTIONS = [
                { text: "Black", value: "black" },
                { text: "White", value: "white" },
            ];
            return {
                cardTypeOptions: CARD_TYPE_OPTIONS,
                selectedCardType: null,
                selectedCardText: null,
            };
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
            handleCreateCard () {
                return fetch(process.env.VUE_APP_SERVER_URL + '/card/create', {
                    method: 'POST',
                    headers: {
                        'content-type': 'application/json'
                    },
                    body: JSON.stringify({
                        cardType: this.selectedCardType,
                        cardContent: this.selectedCardText,
                        deckId: this.deckId
                    })
                }).then(res => {
                    if (!res.ok) {
                        console.error('error creating new card');
                        throw new Error(res.statusText);
                    }
                    return res.json();
                }).then(json => {
                    this.$emit('refresh', json);
                }).catch(err => {
                    this.$emit('error', err);
                });
            },
            formatter (value) {
                return value + " ";
            }
        },
        watch: {
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