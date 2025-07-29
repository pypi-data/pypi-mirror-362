import torch
import torch.nn as nn

import itertools

'''
Notation.

N: batch size;
n: number of features;
m: number of output classes;
nj: number of fuzzy sets for feature j;
R: number of rules;
L: sequence length.
'''

class Antecedents(nn.Module):
    def __init__(self, n_sets, and_operator, mean_rule_activation=False):
        '''Calculates the antecedent values of the rules. Makes all possible combinations from the fuzzy sets defined for              
        each variable, considering rules of the form: var1 is set1 and ... and varn is setn.

        Args:
            n_sets:               list with the number of fuzzy sets associated to each variable.
            and_operator:         torch function for agregation of the membership values, modeling the AND operator.
            mean_rule_activation: bool to keep mean rule activation values.

        Tensors:
            memberships:          tensor (n) with tensors (N, nj) containing the membership values of each variable.
            weight:               tensor (N) representing the activation weights of a certain rule for all inputs.
            antecedents:          tensor (N, R) with the activation weights for all rules.
        '''

        super(Antecedents, self).__init__()

        self.n_sets = n_sets
        self.n_rules = torch.prod(torch.tensor(n_sets)).item()
        self.and_operator = and_operator
        self.combinations = list(itertools.product(*[range(i) for i in n_sets]))
        self.mean_rule_activation = []
        self.bool = mean_rule_activation

    def forward(self, memberships):
        N = memberships[0].size(0)
        antecedents = []
        for combination in self.combinations:
            mfs = [] 
            for var_index, set_index in enumerate(combination):
                mfs.append(memberships[var_index][:, set_index])
            weight = self.and_operator(torch.stack(mfs, dim=1), dim=1)
            if isinstance(weight, tuple):  
                weight = weight[0]  
            antecedents.append(weight)
        antecedents = torch.stack(antecedents, dim=1)
        
        if self.bool:
            with torch.no_grad():
                self.mean_rule_activation.append(torch.mean(antecedents, dim=0))    
        
        return antecedents

class Consequents(nn.Module):
    def __init__(self, n_sets, n_classes):
        '''Calculates the consequents, considering a linear combination of the input variables.

        Args:
            n_sets:       list with the number of fuzzy sets associated to each variable.
            n_classes:    int with number of classes.

        Tensors:
            x:            tensor (N, n) containing the inputs of a variable.
            consequents:  tensor (N, R) containing the consequents of each rule.
        '''

        super(Consequents, self).__init__()

        self.n_vars = len(n_sets)
        self.n_rules = torch.prod(torch.tensor(n_sets)).item()
        self.n_classes = n_classes
        self.mode = 'regression' if n_classes == 1 else 'classification'

        if self.mode == 'regression':
            self.linear = nn.Linear(
                in_features=self.n_vars,
                out_features=self.n_rules,
            )
        
        if self.mode == 'classification':
            self.linear = nn.Linear(
                in_features=self.n_vars,
                out_features=self.n_rules * self.n_classes,
            )
            
    def forward(self, x):
        consequents = self.linear(x)
        return consequents

class Inference(nn.Module):
    def __init__(self, n_classes, output_activation=nn.Identity()):
        '''Performs the Takagi-Sugeno-Kang inference.
        
        Args:
            n_classes:    int with number of classes.
            output_activation: torch function.
        
        Tensors:
            antecedents:       tensor (N, R) with the weights of activation of each rule.
            consequents:       tensor (N, R) with the outputs of each rule.
            Y:                 tensor (N) with the outputs of the system.
            output_activation: torch function.
        '''
        
        super(Inference, self).__init__()
        
        self.n_classes = n_classes
        self.mode = 'regression' if n_classes == 1 else 'classification'
        self.output_activation = output_activation

    def forward(self, antecedents, consequents):
        w = antecedents / torch.sum(antecedents, dim=1, keepdim=True)
        if self.mode == 'classification':
            n_rules = w.shape[1]
            w = w.unsqueeze(-1)
            consequents = consequents.view(-1, n_rules, self.n_classes)
        y_hat = torch.sum(w * consequents, dim=1, keepdim=True).squeeze()
        return self.output_activation(y_hat)
    
class RecurrentInference(nn.Module):
    def __init__(self, n_classes, seq_len, bidirectional=False, output_activation=nn.Identity()):
        '''Performs the Takagi-Sugeno-Kang inference adapted for recurrent models.
        
        Args:
            n_classes:         int with number of classes.
            seq_len:           int with sequence length.
            bidirectional:     bool for directionality of model.
            output_activation: torch function.
        
        Returns:
            y_hat:             tensor (N, L, m) with outputs of the system.
        '''
        
        super(RecurrentInference, self).__init__()
        
        self.n_classes = n_classes
        self.seq_len = seq_len
        self.bidirectional = bidirectional
        self.mode = 'regression' if n_classes == 1 else 'classification'
        self.output_activation = output_activation

    def forward(self, antecedents, consequents, h=None):
        if h is None:
            h = torch.zeros_like(consequents)
        w = antecedents / torch.sum(antecedents, dim=1, keepdim=True)
        n_rules = w.shape[1]
        if self.mode == 'regression':
            if self.bidirectional:
                h = h.view(-1, self.seq_len, 2, n_rules).mean(dim=2)
            consequents = consequents + h
            consequents = consequents.view(antecedents.shape)
        if self.mode == 'classification':
            if self.bidirectional:
                h = h.view(-1, self.seq_len, 2, self.n_classes * n_rules).mean(dim=2)
            w = w.unsqueeze(-1)
            consequents = consequents + h
            consequents = consequents.view(-1, n_rules, self.n_classes)
        y_hat = torch.sum(w * consequents, dim=1, keepdim=True).view(-1, self.seq_len, self.n_classes)
        return self.output_activation(y_hat)