<template>
    <b-card
        :bg-variant="isBlackCard ? 'dark' : 'default'"
        :text-variant="isBlackCard ? 'white' : ''"
        class="player-card text-break"
        :class="{
            'player-card--selectable': canSelect,
            'player-card__judge': isBlackCard,
            'player-card__hand': inHand
        }"
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
            created_at: { type: String, default: "" },
            id: { type: String, default: "" },
            nsfw: { type: Boolean, default: true },
            text: { type: Array, required: true },
            isBlackCard: { type: Boolean, default: false },
            canSelect: { type: Boolean, default: false },
            inHand: { type: Boolean, default: false },
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
                    this.$emit('clicked', this.$vnode.key);
                }
            },
        }
    }
</script>

<style scoped>
    .player-card {
        max-width: 10rem;
        min-height: 14rem;

        min-width: 140px;
        margin: 10px;
    }
    .player-card--selectable {
        cursor: pointer;
    }
    .player-card__judge {
        cursor: default;
    }
    .player-card__hand {
        margin: 10px 0px;
    }
</style>