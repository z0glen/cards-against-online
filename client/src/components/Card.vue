<template>
    <b-card>
        <b-card-text>
            {{ getText() }}
        </b-card-text>
    </b-card>
</template>

<script>
    export default {
        props: {
            created_at: String,
            id: String,
            nsfw: Boolean,
            text: Array,
        },
        methods: {
            getText() {
                return this.text.join("_____");
            }
        }
    }
</script>

<style scoped>

</style>