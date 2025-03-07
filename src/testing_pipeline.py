
from src.pipeline_creator import nlp_factory

# print("starting processing...")
# start_time = timeit.default_timer()
#

text1 = "Cannot\nexclude bicuspid aortic valve."

print(text1)

nlp = nlp_factory()

doc1 = nlp(text1)

print(list(doc1))

for ent in doc1.ents:
    print("ent: {0} --> struc_type: {1} --> struc_text: {2} --> is_uncertain: {3} --> is_negated: {4} --> sentence: {5} --> functional: {6} ".format(ent, ent._.structure_type, ent._.structure_text, ent._.is_uncertain, ent._.is_negated, ent.sent, ent._.is_functional))
    # print("ent: {0} --> is_uncertain: {1} --> is_negated: {2} --> sentence: {3} ".format(ent, ent._.is_uncertain, ent._.is_negated, ent.sent))


# print(text2)
#
# doc2 = nlp(text2)
#
# for ent in doc2.ents:
#     # print("ent: {0} --> window: {1} --> snippet: {2}".format(ent, ent._.window(100, left=True, right=True), ent._.snippet))
#     print("ent: {0} --> is_uncertain: {1} --> is_negated: {2} --> sentence: {3} ".format(ent, ent._.is_uncertain, ent._.is_negated, ent.sent))
#
#
# print(text3)
#
# doc3 = nlp(text3)
#
# for ent in doc3.ents:
#     print("ent: {0} --> is_uncertain: {1} --> is_negated: {2} --> sentence: {3} ".format(ent, ent._.is_uncertain, ent._.is_negated, ent.sent))


# nlp.pipe(text1)
#
#
# stop_time = timeit.default_timer()
#
# print("Completed in: {0} seconds".format(stop_time-start_time))
