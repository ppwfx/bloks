from bloks import gtx
import speech_recognition as sr
from pyphonetics import RefinedSoundex


debug = True

def listen():
    phrases = list(set(gtx.get(["_cmd", "_phrases"])))

    recognizer = sr.Recognizer()
    audio = record(recognizer)
    speech_words = recognize(recognizer, phrases, audio).split()

    if debug:
        print(speech_words)

    print(gtx.get(["_cmd", "_tree"].items()))
    # for tool in gtx.get(["_cmd", "_tree"].items()):
    #     for action in action

    distances = get_distances(phrases, speech_words)
    phrases = get_closest_phrases(speech_words, distances)

    if debug:
        print(phrases)

    return phrases


def record(recognizer):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    return audio




def recognize(recognizer, phrases, audio):
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
      "type": "service_account",
      "project_id": "go-snapper",
      "private_key_id": "7d70ede00db00a75b0f2ad029d7091f3f276e326",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC2MOmp4ZvnYff/\nbMw++MOfuxVY19mElZ+39TAL+bsyOmm37hDPQUq6gxfeYrdd6tjJzt2qm5w6LHTa\nuri98IU4jJzAOiOYfouz8DAA4ZEcv0FFL+V/PXE7hUrTo3vSAxFkMJIdKx4cveiA\nHZmFx7uzx7D4rh5N1/EYtQrD4p8mApbTlhkIKQAtkG1R5TYAB3sFBCiqnZ3C8hjL\n+/19VRiqcBjNDt6xNcRWJfpn8bFY60OCzbySBgyDpAhlffmFsNBMvz/DwbZ8KdEh\nAGhkOFKjV4Pl76bAp0Nl/VES4kfCWFAo97CmQWB8Dtk6/4m3sX7ZZ8p1uvNWJagI\nOZfcxwW9AgMBAAECggEAV+gq3k6ewFp7ZBGVTS8PiLMmnirr57agDY0u5SBWi+o2\nV0p1buMEkRCuxB0id5zYhCsdtnOFwmXv7hfZCsCSLxJdkbybrzkj5CrYppwvvcyk\nTCNLmwTE7WCnlY1UsaTMT+jFn3BOA7U4CRT/HdcdAKYyBBNTSOEQEglMi+59NsOJ\nfrFxSXIs6DQzZj5/s+vgtgB6tE344v/DwUITznPv3ZZCfXhrOSYz0LzRgrOFl4dV\noQ6qzW0YPTdAsQUfc67ODy7D3zElWyr+habfm8kPLWXYbDG+wX5TG8oxF78pWWx8\nlpqZ9vako20VLR9ayI6grVZSUD2cWxZPlMdrxsKwSwKBgQDgUbtf6J2H9hu/qFAa\nhGnc/8OyzlyA0aPJhBefQsal630YXYHN9ZwBWWkdu+vy5JdvPmtjkjyOM26fg/XZ\nacguivU8ajqv4kDBlbDc8kJnmNxjPwR/LDT7HrzczYzXY9Rtn3r5RRY6DWOHbTW2\n1HiHoG9B2zouXJ1UZrWL7Jfx8wKBgQDP7Ajo21FvtHUbSqTyd2OZEzH4q1iwvjdl\nijjSj3umvqghqr5wmBjn5GrAuKCUv6rL69i4jXnPQI9B1TtTQ32oF46W+/sXGQsX\n/7+xcPnChqx7EbVWpYxNIHNPArc7GjubG4JB34fCvqALnbQQKkN1wF1CgoxblBl0\nNBboQ0ZljwKBgCur3dXbPKgWoupaQ1YWR2HuLVRnVp0Bs2htHgg0gOYWhaEzuyy0\nz2130b4nMtVz6YOP3GpjMwTgQH4vu7JbJMzi4sGjUM+jNcY6dVdels0Cdo2f3ClC\nGwJ0xoIaRnw8hEPfU5qp95zPtHvOKDHzBZAqDN7+ZkJWZ47h/CBErIQ/AoGAS035\njByiygpZv6CxTP/gmrhRCPdGD/1UovoEyn4dEq9KxabJgo4TtykLYPF9d2JTwbeR\nroXO8Dk5qWZJLkbrY83kXtq0fhEb6309OE7qpoGQRqKLQu6CegyetqcNJeLCY9L6\nwlDrIqVX4d0kMhaciDE7lbMikqh475VOFqEHBhECgYAT3bMqr8Z1jARoy10HPvHe\nYUkZ4HAvV0mgMGlah7zyEEzTlK0IKTZsc6+opXwF2FEsMxo/75pZxibn5RPJwnqN\nDxtYRRN00hSeT69Z5Zn2ghAsFm+A4vIEwSMoHRy6TlXWlVt9gEi43SgCk3CVPj9P\ns0uEcmThuX39Wh0aQkMHyg==\n-----END PRIVATE KEY-----\n",
      "client_email": "speeoch@go-snapper.iam.gserviceaccount.com",
      "client_id": "111427258053152985135",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/speeoch%40go-snapper.iam.gserviceaccount.com"
    }"""

    speech = recognizer.recognize_google_cloud(audio, language="en-US", credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, preferred_phrases=phrases)

    return speech

def get_distances(phrases, speech_words):
    rs = RefinedSoundex()

    distances = {}
    for phrase in phrases:
        for word in speech_words:
            if word not in distances:
                distances[word] = {}
            distances[word][phrase] = rs.distance(word, phrase)

    return distances

def get_closest_phrases(speech_words, distances):
    phrases = []
    for word in speech_words:
        smallest_distance = 10
        closest_phrase = None
        for phrase, distance in distances[word].items():
            if distance < smallest_distance:
                closest_phrase = phrase
                smallest_distance = distance

        if debug:
            print(closest_phrase, smallest_distance)

        phrases.append(closest_phrase)

    return phrases