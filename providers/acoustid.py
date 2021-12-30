import acoustid
import providers


class AcoustID(providers.LookupProviderInterface):
    def lookup_sample(self, sample):  # -> providers.LookupResult:
        results = {}
        try:
            results = acoustid.match(self.config['api_key'], sample)
        except acoustid.NoBackendError:
            print("chromaprint library/tool not found")
        except acoustid.FingerprintGenerationError:
            print("fingerprint could not be calculated")
        except acoustid.WebServiceError as exc:
            print("web service request failed:", exc.message)

        print(results)
        # first = True
        # for score, rid, title, artist in results:
        #     if first:
        #         first = False
        #     else:
        #         print()
        #     print('%s - %s' % (artist, title))
        #     print('http://musicbrainz.org/recording/%s' % rid)
        #     print('Score: %i%%' % (int(score * 100)))

