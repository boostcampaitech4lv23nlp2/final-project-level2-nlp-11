import datasets
#'imagefolder' <- 허깅페이스에서 만든 이미지 데이터셋 도우미? 라고 보면 될듯.
dataset = datasets.load_dataset('imagefolder', data_dir='datasets/noto_sans',
                                               split='train',
                                               features=datasets.Features({
                                                   'image':datasets.Image(),
                                                   'text':datasets.Value('string')
                                               }))

print(dataset['text'][:5])
# 본인의 데이터셋이름과 본인의 토큰을 입력할 것.
# dataset.push_to_hub('kuotient/noto-emoji-dataset',split='train', token="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")