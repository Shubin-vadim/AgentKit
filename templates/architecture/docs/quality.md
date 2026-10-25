# Quality requirements

<!--
Measurable quality-attribute scenarios (ISO/IEC 25010 characteristics, SEI
six-part form). Pick 3-5 characteristics that matter for this system, not all
eight. Every scenario needs a measure the team can observe (metric, log, or
test); if nobody knows the number yet, write TODO and ask.
Agents fill this file with the `quality-scenarios` skill.
-->

Priority characteristics: <Reliability>, <Security>, <Performance efficiency>.

## Utility tree

<!-- (H,M) = importance for stakeholders, difficulty to achieve. -->

- <Reliability>
  - Q-01 (H,M) <short name>
- <Security>
  - Q-02 (H,L) <short name>

## Scenarios

### Q-01

**Kind:** Usage <!-- Usage | Growth | Exploratory -->
**Characteristic:** <Reliability>

- **Source:** <who or what triggers it: user, operator, failing node, attacker>
- **Stimulus:** <the event>
- **Environment:** <normal | peak | degraded | startup>
- **Artifact:** <container or flow, named as in docs/C4.md>
- **Response:** <what the system does>
- **Measure:** <number, unit, percentile or SLO>

### Q-02

**Kind:** <...>
**Characteristic:** <...>

- **Source:** <...>
- **Stimulus:** <...>
- **Environment:** <...>
- **Artifact:** <...>
- **Response:** <...>
- **Measure:** TODO
