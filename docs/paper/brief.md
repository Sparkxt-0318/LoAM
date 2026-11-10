# Can anyone check a soil-carbon credit? A two-page brief

*Draft for a non-specialist reader. Not for circulation until the PI has reviewed it.*

## The short version

Farmers can earn carbon credits for practices that store more carbon in their soil. Each credit
says, in effect, "the carbon in this soil went up by this much." The only way to know is to dig
soil samples and measure them, and soil is so patchy that a few samples can easily miss a real
change or invent a false one.

We set out to check, for every soil-carbon project we could find, whether the sampling behind
the credits could have detected the change being credited. **We mostly could not, because the
sampling details are not published.** So we asked the next-best question: how much sampling
*would* have been needed? On that question, most credited changes we could test turn out to be
cheap to detect, and a few small ones do not.

## Three findings

**1. Australia publishes no sampling details for any soil-carbon project.**
Australia's official register lists 999 soil-carbon projects. 54 of them have been issued 462,162
credits. The register has no place at all to record how many soil samples were taken, how deep,
or how often. The fields are not blank; they do not exist. The rules require each project to
have a sampling plan, but the plans are never published. US and European registries publish
more, but the key numbers are still kept in documents the public cannot see.

**2. The same soil gets a very different discount depending on the registry.**
Every registry takes a discount for measurement uncertainty: the less precise the measurement,
the fewer credits issued. That is sensible. But for exactly the same soil and exactly the same
measurements, the strictest of the three registries takes a discount **four times larger** than
the most lenient. The difference comes from the registry's rulebook, not the soil.

**3. Where we could check, most claims are easy to detect, and a few small ones are not.**
For the 56 projects that publish enough to run the numbers, we worked out the cheapest sampling
campaign that would have detected each project's credited change. We assumed soil as uniform as
the scientific evidence allows, which is deliberately generous to the project. For most
projects:
- the needed campaign is modest;
- it would cost a few cents to a dollar per credit;
- that is far below any carbon price.

For three small, young projects in our cropland focus, the credited change so far is small. A
campaign to detect it would need more samples per hectare than any project has ever disclosed.

Two projects publish the discount they actually took. That number reveals how precise the
project itself says its measurement was. For one project, the credited change is about three
times the smallest change its own precision could detect. For the other, the credited change
appears to be smaller than its own detection limit, but that reading depends on two technical
points we have not yet been able to confirm from the original documents.

## What this does and does not mean

- **It is not an accusation against any project or company.** We could not see any project's
  actual sampling. "Hard to detect" means "would need dense sampling", not "did not happen".
- **The biggest uncertainty is scale.** Our soil-patchiness numbers come from small research
  plots, a few hundred square metres. The projects cover whole farms and regions. The published
  evidence says soil is patchier at farm scale than on research plots, probably several times
  over. Even so, most of our cropland projects stay detectable when we allow for that: 6 of 11
  in the worst case we tried, against 8 of 11. What nobody has measured is how patchy the
  *change* in soil carbon is at farm scale. Until someone does, every "easy to detect" carries
  that condition.
- **Most of the record could not be checked at all.** Verra, the largest international registry,
  moved to a new website this year that we could not search automatically. Its roughly 200
  soil-carbon projects are missing because of access, not because they publish nothing.

## What would fix it

The registries already contain the right formula for how many samples are needed to detect a
change. What is missing is publication of the inputs. **About nine numbers per project would let
anyone run that check themselves**, using the registry's own formula and none of ours:
- how many locations were sampled, and how many cores were mixed into each sample;
- how deep they sampled, and how depth was accounted for;
- when the samples were taken;
- how variable the results were;
- the smallest change the design could detect;
- the uncertainty discount, split by source;
- the area in hectares;
- whether the model's predictions were later checked against new measurements.

None of these would reveal farmers' private data or field locations.

---

*Numbers in this brief come from `docs/phase5_population_results.md`, `docs/registry_population.md`
and `data/registry/projects.yaml`. The "four times" is the ratio of CAR's 1.028 to ACCU's 0.253
relative standard errors (D-057). The "about three times" is CAR1459's 2.81 (D-068). The "smaller
than its own detection limit" is VCS 4022's 0.42, which depends on PI decision A; if that
decision goes the other way, delete that sentence.*
