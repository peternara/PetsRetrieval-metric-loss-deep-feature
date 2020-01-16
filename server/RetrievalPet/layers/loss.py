import torch
import torch.nn as nn

import RetrievalPet.layers.functional as LF

# --------------------------------------
# Loss/Error layers
# --------------------------------------

class ContrastiveLoss(nn.Module):
    r"""CONTRASTIVELOSS layer that computes contrastive loss for a batch of images:
        Q query tuples, each packed in the form of (q,p,n1,..nN)

    Args:
        x: tuples arranges in columns as [q,p,n1,nN, ... ]
        label: -1 for query, 1 for corresponding positive, 0 for corresponding negative
        margin: contrastive loss margin. Default: 0.7

    >>> contrastive_loss = ContrastiveLoss(margin=0.7)
    >>> input = torch.randn(128, 35, requires_grad=True)
    >>> label = torch.Tensor([-1, 1, 0, 0, 0, 0, 0] * 5)
    >>> output = contrastive_loss(input, label)
    >>> output.backward()
    """

    def __init__(self, margin=0.7, eps=1e-6):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin
        self.eps = eps

    def forward(self, x, label):
        return LF.contrastive_loss(x, label, margin=self.margin, eps=self.eps)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'margin=' + '{:.4f}'.format(self.margin) + ')'

class ContrastiveLoss_couple(nn.Module):
    r"""CONTRASTIVELOSS layer that computes contrastive loss for a batch of images:
        Q query tuples, each packed in the form of (q,p,n1,..nN)

    Args:
        x: tuples arranges in columns as [q,p,n1,nN, ... ]
        label: -1 for query, 1 for corresponding positive, 0 for corresponding negative
        margin: contrastive loss margin. Default: 0.7

    >>> contrastive_loss = ContrastiveLoss(margin=0.7)
    >>> input = torch.randn(128, 35, requires_grad=True)
    >>> label = torch.Tensor([-1, 1, 0, 0, 0, 0, 0] * 5)
    >>> output = contrastive_loss(input, label)
    >>> output.backward()
    """

    def __init__(self, margin=0.7, eps=1e-6, margin2=0.3, beta=0.75):
        super(ContrastiveLoss_couple, self).__init__()
        self.margin = margin
        self.eps = eps
        self.margin2 = margin2
        self.beta = beta
    def forward(self, x, label):
        return LF.contrastive_loss_couple(x, label, margin=self.margin, eps=self.eps, margin2=self.margin2, beta=self.beta)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'margin=' + '{:.4f}'.format(self.margin) + ')'
class BeidaLoss_couple(nn.Module):
    r"""CONTRASTIVELOSS layer that computes contrastive loss for a batch of images:
        Q query tuples, each packed in the form of (q,p,n1,..nN)

    Args:
        x: tuples arranges in columns as [q,p,n1,nN, ... ]
        label: -1 for query, 1 for corresponding positive, 0 for corresponding negative
        margin: contrastive loss margin. Default: 0.7

    >>> contrastive_loss = ContrastiveLoss(margin=0.7)
    >>> input = torch.randn(128, 35, requires_grad=True)
    >>> label = torch.Tensor([-1, 1, 0, 0, 0, 0, 0] * 5)
    >>> output = contrastive_loss(input, label)
    >>> output.backward()
    """

    def __init__(self, margin=0.7, eps=1e-6):
        super(BeidaLoss_couple, self).__init__()
        self.margin = margin
        self.eps = eps
    def forward(self, x, label):
        return LF.beida_loss_couple(x, label, margin=self.margin, eps=self.eps)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'margin=' + '{:.4f}'.format(self.margin) + ')'

class BaiduLoss(nn.Module):

    def __init__(self, margin=0.7, eps=1e-6):
        super(BaiduLoss, self).__init__()
        self.margin = margin
        self.eps = eps
    def forward(self, x, label):
        return LF.baidu_loss(x, label, margin=self.margin, eps=self.eps)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'margin=' + '{:.4f}'.format(self.margin) + ')'

class TriangleLoss(nn.Module):

    def __init__(self, margin=0.7, eps=1e-6):
        super(TriangleLoss, self).__init__()
        self.margin = margin
        self.eps = eps
    def forward(self, x, label):
        return LF.triangle_loss(x, label, margin=self.margin, eps=self.eps)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'margin=' + '{:.4f}'.format(self.margin) + ')'


class TriangleLossNpairs(nn.Module):

    def __init__(self, margin=1.7, l2_reg=0.02):
        super(TriangleLossNpairs, self).__init__()
        self.l2_reg = l2_reg
        self.margin = margin
    def forward(self, embeddings, target):
        return LF.triangle_loss_npairs_new(embeddings, target, margin=self.margin, l2_reg=self.l2_reg)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'l2_reg=' + '{:.4f}'.format(self.l2_reg) + ')'

class TripletLossNpairs(nn.Module):

    def __init__(self, l2_reg=0.02):
        super(TripletLossNpairs, self).__init__()
        self.l2_reg = l2_reg
    def forward(self, embeddings, target):
        return LF.triplet_loss_npairs_new(embeddings, target, l2_reg=self.l2_reg)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'l2_reg=' + '{:.4f}'.format(self.l2_reg) + ')'

class BaiduLossNpairs(nn.Module):
    def __init__(self, angle_bound=1., l2_reg=0.02):
        super(BaiduLossNpairs, self).__init__()
        self.l2_reg = l2_reg
        self.angle_bound = angle_bound
    def forward(self, embeddings, target):
        return LF.angular_loss_npairs_new(embeddings, target, angle_bound=self.angle_bound, l2_reg=self.l2_reg)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'l2_reg=' + '{:.4f}'.format(self.l2_reg) + ')'