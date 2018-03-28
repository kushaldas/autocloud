
0.8.0
-----

Pull Requests

- (@vivekanand1101) #60, Fix config file
  https://github.com/kushaldas/autocloud/pull/60
- (@sayanchowdhury) #62, autocloud: Fix the autocloud consumer for the F28 messages
  https://github.com/kushaldas/autocloud/pull/62

Commits

- 1ead83200 config: Fix typo, cofig => config
  https://github.com/kushaldas/autocloud/commit/1ead83200
- 2a9b88437 config: Fix loading of default config values
  https://github.com/kushaldas/autocloud/commit/2a9b88437
- 537134eb7 autocloud: Fix the autocloud consumer for the F28 messages
  https://github.com/kushaldas/autocloud/commit/537134eb7

0.7.4
-----

Pull Requests

- (@sayanchowdhury) #58, Fix the queryset to ignore globally instead of just compose id 
  https://github.com/kushaldas/autocloud/pull/58

Commits

- 615b2bebc web: Fix the queryset to ignore globally instead of just compose id
  https://github.com/kushaldas/autocloud/commit/615b2bebc

0.7.3
-----

Pull Requests

- (@sayanchowdhury) #57, Only show the supported archs in the webapp
  https://github.com/kushaldas/autocloud/pull/57

Commits

- 5e7dbbcc4 web: Exclude the archs that are not supported in the webapp too
  https://github.com/kushaldas/autocloud/commit/5e7dbbcc4

0.7.2
-----

Pull Requests

- (@sayanchowdhury) #56, Ignore if the arch is not supported
  https://github.com/kushaldas/autocloud/pull/56

Commits

- 84281ac05 Don't process arch which are not supported
  https://github.com/kushaldas/autocloud/commit/84281ac05

0.7.1
-----

Pull Requests

- (@sayanchowdhury) #51, Sync 0.6 release
  https://github.com/kushaldas/autocloud/pull/51
- (@sayanchowdhury) #52, Add new entries to the MANIFEST file
  https://github.com/kushaldas/autocloud/pull/52

Commits

- 3d48bfc67 Removes sha-bang line
  https://github.com/kushaldas/autocloud/commit/3d48bfc67
- 622b99d9f If no result file, just save that info to db
  https://github.com/kushaldas/autocloud/commit/622b99d9f
- f0e1cac3e Add new entries to the MANIFEST file
  https://github.com/kushaldas/autocloud/commit/f0e1cac3e

0.7.0
-----

Pull Requests

- (@yahzaa)         #49, Refactor AutoCloudConsumer
  https://github.com/kushaldas/autocloud/pull/49
- (@puiterwijk)     #50, Add artifact information to compose.complete message
  https://github.com/kushaldas/autocloud/pull/50
- (@sayanchowdhury) #46, Explicitly close the DB connections
  https://github.com/kushaldas/autocloud/pull/46

Commits

- 144aa8eb8 Reduce nesting in AutoCloudConsumer.consume
  https://github.com/kushaldas/autocloud/commit/144aa8eb8
- 874ee5ffb Add artifact information to compose.complete message
  https://github.com/kushaldas/autocloud/commit/874ee5ffb
- 53cf57544 pep8
  https://github.com/kushaldas/autocloud/commit/53cf57544
- 060c9014e Explicitly close the DB connections
  https://github.com/kushaldas/autocloud/commit/060c9014e
