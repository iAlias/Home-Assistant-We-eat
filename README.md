# Home Assistant We Eat

This custom integration shows a random recipe from a configurable list. The recipe updates every day at **12:00** and **19:00** for lunch and dinner.

## Installation

1. Copy the `custom_components/we_eat` folder to your Home Assistant `config/custom_components` directory **or** add this repository as a custom integration in HACS (thanks to the included `hacs.json`).
2. Copy `we_eat_card.js` to your `www` folder and add the resource to your Lovelace configuration.

## Configuration

Add to your `configuration.yaml`:

```yaml
we_eat:
  recipes:
    - Spaghetti
    - Pizza
    - Risotto
```

Reload Home Assistant. A sensor named `sensor.we_eat_menu` will be created.

Use the provided services `we_eat.add_recipe`, `we_eat.remove_recipe`, and `we_eat.set_recipes` to manage recipes or edit them directly from the card when `editable: true`.

Add the custom card to your dashboard:

```yaml
type: 'custom:we-eat-card'
entity: sensor.we_eat_menu
editable: true
```
