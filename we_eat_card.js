class WeEatCard extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    const entity = hass.states[this.config.entity];
    if (!entity) return;
    if (!this.content) {
      this.innerHTML = `
        <ha-card header="We Eat">
          <div class="card-content"></div>
          <div class="edit" style="display:none">
            <input type="text" placeholder="Add recipe">
            <button class="add">Add</button>
            <ul class="list"></ul>
          </div>
        </ha-card>`;
      this.content = this.querySelector(".card-content");
      this.edit = this.querySelector(".edit");
      this.input = this.querySelector("input");
      this.list = this.querySelector(".list");
      this.querySelector(".add").addEventListener("click", () => {
        const val = this.input.value.trim();
        if (val) {
          this._hass.callService("we_eat", "add_recipe", { recipe: val });
          this.input.value = "";
        }
      });
    }
    this.content.innerHTML = entity.state;
    if (this.config.editable) {
      this.edit.style.display = "block";
      this.renderList(entity.attributes.recipes || []);
    }
  }

  renderList(recipes) {
    this.list.innerHTML = "";
    recipes.forEach((r) => {
      const li = document.createElement("li");
      li.textContent = r;
      const b = document.createElement("button");
      b.textContent = "x";
      b.addEventListener("click", () => {
        this._hass.callService("we_eat", "remove_recipe", { recipe: r });
      });
      li.appendChild(b);
      this.list.appendChild(li);
    });
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
