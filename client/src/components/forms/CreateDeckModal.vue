<template>
    <b-modal
        :id="id"
        title="Create Deck"
        okTitle="Create"
        @ok="handleCreateDeck"
    >
        <b-form>
            <b-form-group
                label="Name"
            >
                <b-form-input
                    v-model="deckName"
                />
            </b-form-group>
        </b-form>
    </b-modal>
</template>

<script>
    export default {
        props: {
            id: { type: String, required: true },
        },
        data () {
            return {
                deckName: "",
            };
        },
        computed: {
        },
        methods: {
            handleCreateDeck () {
                return fetch(process.env.VUE_APP_SERVER_URL + '/deck/create', {
                    method: 'POST',
                    headers: {
                        'content-type': 'application/json'
                    },
                    body: JSON.stringify({name: this.deckName})
                }).then(res => {
                    if (!res.ok) {
                        console.error('error creating new deck');
                        throw new Error(res.statusText);
                    }
                    return res.json();
                }).then(json => {
                    this.$emit('refresh', json);
                }).catch(err => {
                    this.$emit('error', err);
                });
            }
        }
    };
</script>

<style scoped>

</style>