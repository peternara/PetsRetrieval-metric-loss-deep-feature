import torch
from tqdm import tqdm
import matplotlib.pyplot as plt
from imutils import paths
import numpy as np
import argparse
import pickle
import os
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms
from build_vocab import Vocabulary
from model import EncoderCNN, DecoderRNN
from PIL import Image
import json
import time
import pdb

def to_var(x, volatile=False):
    if torch.cuda.is_available():
        x = x.cuda()
    return Variable(x, volatile=volatile)

def load_image(image_path, transform=None):
    image = Image.open(image_path)
    image = image.resize([224, 224], Image.LANCZOS)

    if transform is not None:
        image = transform(image).unsqueeze(0)

    return image

def load_image_paths(paths, transform=None):
    res = []
    for img_path in paths.list_images(paths):
        image = Image.open(img_path)
        image = image.resize([224, 224], Image.LANCZOS)

        if transform is not None:
            image = transform(image).unsqueeze(0)
        image_tensor = to_var(image, volatile=True)
        res.append(image_tensor)
    return res

def main(args):
    vectore_dir = '/root/server/best_model/'


    # Image preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))])

    # Load vocabulary wrapper
    with open(args.vocab_path, 'rb') as f:
        vocab = pickle.load(f)

    # Build Models
    # encoder = EncoderCNN(args.embed_size)
    qvecs_pca = np.load(os.path.join(vectore_dir, "q_2{}.npy".format(args.embed_size)))
    # encoder.eval()  # evaluation mode (BN uses moving mean/variance)
    decoder = DecoderRNN(args.embed_size, args.hidden_size,
                         len(vocab), args.num_layers)


    # Load the trained model parameters
    # encoder.load_state_dict(torch.load(args.encoder_path))
    decoder.load_state_dict(torch.load(args.decoder_path))

    # Prepare Image
    #image = load_image(args.image, transform)
    #image_tensor = to_var(image, volatile=True)

    # If use gpu
    if torch.cuda.is_available():
        # encoder.cuda()
        decoder.cuda()

    data = []
    # img_path = args.image
    # # Prepare Image
    # image = load_image(img_path, transform)
    # image_tensor = to_var(image, volatile=True)
    # Generate caption from image
    # feature = encoder(image_tensor)
    num=29
    feature = torch.from_numpy(qvecs_pca[num:num+1,:]).cuda()
    #pdb.set_trace()
    sampled_ids = decoder.sample(feature)
    sampled_ids = sampled_ids.cpu().data.numpy()

    # Decode word_ids to words
    sampled_caption = []
    for word_id in sampled_ids:
        word = vocab.idx2word[word_id]
        if word == '<start>':
            continue
        if word == '<end>':
            break
        sampled_caption.append(word)
    sentence = ' '.join(sampled_caption)
    # Print out image and generated caption.
    print (sentence)
    # data.append({'key': img_path.split('/')[-1], 'sentence': sentence})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str,
                        help='input image for generating caption')
    parser.add_argument('--encoder_path', type=str, default='./models/encoder-5-3000.pkl',
                        help='path for trained encoder')
    parser.add_argument('--decoder_path', type=str, default='./models/decoder-5-3000.pkl',
                        help='path for trained decoder')
    parser.add_argument('--vocab_path', type=str, default='./data/vocab.pkl',
                        help='path for vocabulary wrapper')

    # Model parameters (should be same as paramters in train.py)
    parser.add_argument('--embed_size', type=int , default=256,
                        help='dimension of word embedding vectors')
    parser.add_argument('--hidden_size', type=int , default=512,
                        help='dimension of lstm hidden states')
    parser.add_argument('--num_layers', type=int , default=1 ,
                        help='number of layers in lstm')
    parser.add_argument('--save_file', type=str, default='./results/pets_captions.json',
                        help='Json file to save image captions')
    args = parser.parse_args()
    main(args)
