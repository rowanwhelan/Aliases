### TODO List

---

#### 1. Overhaul of Automated Bot Opponents
- **Enhance Bot Intelligence**:
  - Implement a **clue-giving bot** that suggests words based on team-related probabilities and semantic similarities.
  - Improve the **guessing bot** logic by incorporating advanced NLP techniques like BERT or GloVe embeddings.
  - Introduce **adaptive difficulty** levels for bots:
    - Easy: Basic word matching.
    - Medium: Contextual similarity with moderate strategy.
    - Hard: Advanced strategy and bluffing simulation.
- **Mass Simulations**:
  - Automate the creation of large-scale bot-only games.
  - Use these simulations to populate the **statistics page** with gameplay data.

---

#### 2. Overhaul of Gameplay Mechanics
- **Specialized Word Sets**:
  - Add themed word sets (e.g., **Movies**, **Science**, **Fantasy**) for tailored experiences.
- **New Game Modes**:
  - **Timed Mode**: Players must guess within a set time limit.
  - **Sudden Death**: Each incorrect guess has an escalating penalty.
  - **Team Power-Ups**: Abilities like revealing hints or blocking opponents for a turn.
- **Word Elimination**:
  - Allow dynamic elimination of used or less relevant words to keep the game engaging.
- **Custom Games**:
  - Let players design their own boards with custom word lists and rules.

---

#### 3. Implementation of Online Play and Account Saving
- **Online Multiplayer**:
  - Introduce real-time online matches using WebSocket for seamless communication.
  - Add matchmaking with skill-based pairing.
- **Account System**:
  - Create user accounts with persistent data storage.
  - Track **game history**, **win/loss stats**, and **custom settings**.
- **Friend System**:
  - Enable users to add friends and invite them to private games.
- **Leaderboard**:
  - Display global, regional, and friend-based rankings.

---

#### 4. Overhaul Frontend from Flask to Django
- **Migrate Backend**:
  - Transition from Flask to Django for enhanced scalability and ORM support.
- **Improve Templates**:
  - Utilize Django templates for dynamic page rendering.
  - Implement reusable components to streamline UI updates.
- **Frontend Framework**:
  - Integrate modern frontend frameworks (React or Vue) with Django for a more interactive experience.
- **API Layer**:
  - Develop a REST or GraphQL API using Django Rest Framework for better modularity.

---

#### Styling Updates
- **UI Overhaul**:
  - Refresh overall styling for a modern and intuitive design.
  - Enhance color-coding and typography for clarity and aesthetic appeal.
  - Ensure responsive design for optimal performance across devices.