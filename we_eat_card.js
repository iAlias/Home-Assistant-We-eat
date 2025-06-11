class WeEatCard extends HTMLElement {
  set hass(hass) {
    const entity = hass.states[this.config.entity];
    if (!entity) return;
    if (!this.content) {
      this.innerHTML = `
        <ha-card header="We Eat">
          <div class="card-content"></div>
        </ha-card>`;
      this.content = this.querySelector(".card-content");
    }
    this.content.innerHTML = entity.state;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error("Entity is required");
    }
    this.config = config;
  }

  static getConfigElement() {
    return document.createElement("hui-entities-card-editor");
  }
}
customElements.define('we-eat-card', WeEatCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'we-eat-card',
  name: 'We Eat Card',
  description: 'Shows random recipe from We Eat sensor.',
});
