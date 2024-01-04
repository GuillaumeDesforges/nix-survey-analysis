![e74772af083ce1fbf7e82ddbdbae73d368671194|690x221](upload://yJcxsbtumBNbpu7OMlUmNkFBKrd.png)

# 2023 Nix Survey Results

The Nix community is growing at an exciting pace, which makes it harder and more important to understand who comprises our community, what people use and care about, and the main pain points that frustrate users or impede progress and adoption. Therefore, the Nix Marketing Team conducts a yearly survey to better undestand these issues. Your feedback helps develop Nix, Nixpkgs, and NixOS to match your needs and come up with new ideas for better serving and growing the community.

## tl;dr

* Compared to last year, we had more respondents, of which a good proportion were newcomers.
* The community may slowly trend towards more diversity in terms of technical background and occupation.
* The Nix ecosystem is still difficult to navigate and work with (developer experience, sparse or unclear documentation, lack of recipes)
* Nonetheless, most respondents consider that the benefits of using Nix/NixOS outweigh all the downsides.

We will try to make next year’s survey easier to complete and tailor it to better support the other community teams. Communication should also be improved to increase outreach and get more people to respond.

## Total Participation, Response Rate

We received 2493 responses, an increase of 15% compared to last year.

Taking into account the fact that most questions are conditionally prompted depending on a respondent previous answers, on average questions were answered 67% of the time. Without much surprise, the simplest questions (single choice questions) had the most engagement from respondents, but the order of the questions seem to matter as well (R²=0.30).

> **Warning**
>
> For many questions, respondents could select multiple choices. As such, in this analysis, percentages for such questions are percentages of “Yes” answers for the choice itself, represented in green. This explains why percentages for a seemingly unique question will not add up to 100%.
> 
> Single choice question are represented in blue, and the sum of all percentages is 100%.

## The Shape of the Nix Community

Respondents were either from Europe (50%) or North America (23%) for the most part.

Given that many respondents did not state their gender (14%), there is a lot of uncertainty on the exact results. That being said, it is clear that most respondents were men (>80%). We may consider discarding this question, as did Stack Overflow and other surveys.

GNU/Linux is used by a large part of the community (80%), but other operating systems like Windows (27%) or macOS (26%) are also quite widespread. Surprisingly, about 50 respondents were Windows-only users.

Most people in the community are Backend Developers (31%), which is less than last year (was 40%, meaning a drop by 25%).

Overall, the “shape” of our community is largely the same as last year. However, we do see a reduced concentration of the previously most common profiles, which have a lower percentage than last year. One could say that the distribution is “flattening” a bit, which means that the Nix user base seems to be a bit more diverse. It will be interesting in coming years to see if this is an actual trend or not.

<!-- plots -->
![region|690x345](upload://h9TYmaBfqK9kImGnY9v1PnR6Rnc.png)
![age|690x345](upload://voKl5KEz5bTfaBvqFON9U1hhG9z.png)
![gender|690x345](upload://jJFPH8eOYGykxvrKKLCdllPTNc1.png)
![occupation|625x500, 100%](upload://ldcnvBRMUx0R19JqFUgEBV5wMxt.png)
![os|625x500, 100%](upload://lIDoUeF4wxU3z98iEjFpGudNj82.png)


## Nix at Work

The majority of respondents who use Nix do so on a daily basis (77%). As mentioned last year, this aligns with the expectation that those most interested in providing feedback are frequent users. Keep this in mind when reviewing the data and takeaways.

Most respondents have been using Nix for less than a year (38%), which hints at an increase of new users. Unfortunately we didn’t receive as many answers from users who have been using Nix for 1-3 years as we would have expected. Indeed, last year’s respondents who were, at the time, users with less than a year of experience should now have been part of the “1-3 years” group, making it grow accordingly. This would mean that many respondents with now 1-3 years of experience did not respond to the survey this year.

57% of respondents said they use Nix for work. At the same time, respondents said that they use Nix for at least one of their personal projects (88%). This could be interpreted that Nix users are very enthusiastic and want to use Nix, but either they deem it not ready for industrial use or Nix is not part of the tech stack at their workplace.

<!-- plots -->
![frequencyNix|690x345](upload://6My7IsdQWJjxERFfTyPmjbxBmVe.png)
![durationNix|690x345](upload://zilbIK6LJ2ntedwCigVkv20h4QT.png)
![contextNix|625x500](upload://vOH3eb9vJvdeXdtICcK68jnGgM8.png)


## Key Themes

Last year, we had noticed 5 key themes:

* The “superpower”: Nix/NixOS is declarative and reproducible
* Nix/NixOS has a steep learning curve
* Nix/NixOS needs better documentation
* Nix is hard to debug
* It is hard to contribute back to the Nix ecosystem

This year is not too different: most Nix users love it for what it does well. Nix is used because it allows declarative configuration of reproducible systems and builds. Once you fix something, it stays fixed!

However, even the most enthusiastic Nix users agree on the fact that it has a very steep learning curve at every step. It is hard to get into Nix as a user, as a developer, and as a maintainer.

For each participant profile, people largely agree that the Nix documentation is one of the biggest issue. Sometimes because it is lacking, sometimes because it is unclear or not up to date. More specifically for beginners, it lacks comprehensive, accessible examples and recipes.

The barriers for wider adoption are that it is too difficult to make things work for particular use cases, or that documentation is not good enough.

## Next Steps

Our goal is to help all of us understand what the community needs and wants. This information will benefit all parts of the Nix ecosystem, helping teams plan and prioritise efforts to meet the community’s needs.

We’ll be doing the Nix Community Survey again next year, and we’re working on making it even better. We gathered a lot of feedback from the last question of the survey, and plan to act on it.

I would like to thank everyone who helped make it happen yet again, and hope to see you all again next year! ♥️

## Results

Below are all the quantitative results.

<!-- plots -->
![region|690x345](upload://h9TYmaBfqK9kImGnY9v1PnR6Rnc.png)
![age|690x345](upload://voKl5KEz5bTfaBvqFON9U1hhG9z.png)
![gender|690x345](upload://jJFPH8eOYGykxvrKKLCdllPTNc1.png)
![occupation|625x500](upload://ldcnvBRMUx0R19JqFUgEBV5wMxt.png)
![os|625x500](upload://lIDoUeF4wxU3z98iEjFpGudNj82.png)
![regularUseNix|690x345](upload://hwXAJKjxdxQ5BT4Mh3aN9nlw610.png)
![triedStopNix|690x345](upload://g7InlxmD50LtH2NcGdwXWUkFZK1.png)
![trialNix|625x500](upload://izcRmm48ZtHnOSzjUsz70HCd5A2.png)
![triedStopTrialNix|625x500](upload://jH3pWn0ZdDgJEI3sFCBp7Btf64t.png)
![frequencyNix|690x345](upload://6My7IsdQWJjxERFfTyPmjbxBmVe.png)
![contextNix|625x500](upload://vOH3eb9vJvdeXdtICcK68jnGgM8.png)
![durationNix|690x345](upload://zilbIK6LJ2ntedwCigVkv20h4QT.png)
![osNix|625x500](upload://bkzusEpzIuQJ1InRYkU8Kdm1Bo2.png)
![environNix|625x500](upload://sTNtFUShgl2JTmmtqQ4hYWdcvn8.png)
![useNix|625x500](upload://i8MwZaCDHLgqXyr6Gy3PUMtPQzK.png)
![whichChannel|690x345](upload://dqLZCoPHSNZ4s2kUzA11QMVcg5W.png)
![ciNix|625x500](upload://vJk96MXfHBuHYSpGzEmcS1QwxRA.png)
![extendNix|625x500](upload://z76fqAEKph0nrvuc18edZbt02gS.png)
![experimentalNix|625x500](upload://z6PopRYZqhkWvBR3aCBIEUUGJFv.png)
![involvement|690x345](upload://yRmMZao54w4Q3buIBw8yc1LAH8c.png)
![regularNixOS|690x345](upload://u9ExQPSIvr6Z6PVbKGoo1gdKLEa.png)
![triedStopNixOS|690x345](upload://hugR3586FiZQo7jyyocamnqD1mG.png)
![frequencyNixOS|690x345](upload://nmaaKlznx9pbJr1xR6Osnslzqmg.png)
![contextNixOS|625x500](upload://6eQ9gAOjWD7lnyrMm3Mb8Dr7XIf.png)
![durationNixOS|690x345](upload://adeLo15gO4WCeA8P1tniUNo0XDr.png)
![environNixOS|625x500](upload://vEs2gglu5pkK8sD1UYLvcMwl0AD.png)
![deploymentsNixOS|625x500](upload://qX4KkIcKpocJEpY5Kmq8Y6t5DPg.png)
![desktopNixOS|625x500](upload://jpkb9625GI9xijxJS3qfIDKMCxy.png)


## Method

The Nix Marketing Team conducted an online survey of 47 questions, of which 13 were single choice questions, 17 multiple choices, 4 ranking and 13 open-ended.

The survey was open for a one month period from June 11th until July 10th. We announced the survey by way of postings to Nix Discourse, Matrix, LinkedIn and Twitter.

The survey was split into four subsections:

* Background Information
* Nix User Questions
* NixOS User Questions
* Misc. Questions

Once the survey window was closed we split the analysis into two: multiple choice questions and open-ended questions. Multiple choice was analyzed numerically by compiling the responses by count and percentages, and comparing to previous year’s results. Open-ended questions were analyzed by manually reviewing the responses. The survey analysis was conducted throughout the month of August.

## Final words

Huge thanks to all the people who contributed to the survey: @kranzes @ron @fricklerhandwerk @garbas @Arsleust 

If you’d like to help organize next year’s survey please contact the marketing team on Matrix: [`#marketing:nixos.org`](https://matrix.to/#/#marketing:nixos.org)

See you next year!
