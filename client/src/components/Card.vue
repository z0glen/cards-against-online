<template>
    <b-card
        :bg-variant="isBlackCard ? 'dark' : 'default'"
        :text-variant="isBlackCard ? 'white' : ''"
        class="player-card"
        :class="{canSelect, isBlackCard}"
        @click="handleClick"
    >
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
            isBlackCard: Boolean,
            canSelect: Boolean,
        },
        computed: {
            variant() {
                return this.isBlackCard ? "dark" : "default";
            }
        },
        methods: {
            getText() {
                return this.text.join("_____");
            },
            handleClick() {
                if (this.canSelect) {
                    alert(this.text);
                    this.$emit('clicked', this.id);
                }
            },
        }
    }
</script>

<style scoped>
    .player-card {
        overflow-wrap: break-word;
        word-wrap: break-word;
        hyphens: auto;

        cursor: not-allowed;
    }

    .canSelect {
        cursor: pointer;
    }

    .isBlackCard {
        cursor: default;
    }
</style>