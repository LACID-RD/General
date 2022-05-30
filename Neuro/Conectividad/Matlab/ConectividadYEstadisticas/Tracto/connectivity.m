%Import connectivity matrix
A = load('Lopez_fdt_network_matrix'); 
%Matrix normalization (rescales all weight magnitudes to range [0,1])
UmbralConect=0;%Para evitar falsos positivos
Waytotal=load('Lopez_waytotal'); %Cargo el waytotal
[mm,nn]=size(A);
W=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if A(i,j)>UmbralConect
                W(i,j)=A(i,j)/Waytotal(i);
        else
            W(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        W(i,j)=(W(i,j)+W(j,i))/2;
        W(j,i)=W(i,j);
        if i==j
            W(i,j)=1;
        end
    end
end
%Matrix L: conversion of connection weights to connection lengths (needed
%for weighted distance-based measures (higher weights are interpreted as
%shorter lengths). This matrix is defined as the inverse of the
%connection-weights matrix:
L_14 = weight_conversion(W,'lengths');

%Fix matrix (remove all Inf and NaN values, remove all self-connections,
%ensures that matrices are exactly symmetric):
W_fix_14 = weight_conversion(W, 'autofix');

%%%%%%%MEASURES%%%%%%%%%%%
%Degree - number of links connected to the node (connection weights are
%ignored):
deg_14 = degrees_und(W_fix_14);

%Strength - sum of weights of links connected to the node:
str_14 = strengths_und(W_fix_14);

%Density - fraction of present connections to possible connections
%(connection weights are ignored):

[density_14, vert_14, edges_14] = density_und(W_fix_14);

%Clustering coefficient - fraction of triangles around a node; equivalent
%to the fraction of node's neighbors that are neighbors of each other.

cluster_coef_14 = clustering_coef_wu(W_fix_14);

%Global and local efficiency - Global efficiency is the average inverse
%shortest path length in the network and is inversely related to the
%characteristic path length. The local efficiency is the global efficiency
%computed on neighborhood of the node and is related to the clustering
%coefficient.

global_efficiency_14 = efficiency_wei(W_fix_14);
local_efficiency_14 = efficiency_wei(W_fix_14,2);

%Distance matrix: 
%   The distance matrix contains lengths of shortest paths between all
%   pairs of nodes. An entry (u,v) represents the length of shortest path 
%   from node u to node v. The average shortest path length is the 
%   characteristic path length of the network.
%   Output:     distance_matrix,      distance (shortest weighted path) matrix
%               edges_distance,      number of edges in shortest weighted path matrix

[distance_matrix_14, edges_distance_14] = distance_wei(L_14);

%Betweenness centrality
%   Node betweenness centrality is the fraction of all shortest paths in 
%   the network that contain a given node. Nodes with high values of 
%   betweenness centrality participate in a large number of shortest paths.

BC_14 = betweenness_wei(L_14);





%DEFINITION OF FUNCTIONS (They belong to the Brain Connectivity Toolbox (BCT)):

%weight_conversion
function W = weight_conversion(W, wcm)
switch wcm
    case 'binarize'
        W=double(W~=0);         % binarize
    case 'normalize'
        W=W./max(abs(W(:)));    % rescale by maximal weight
    case 'lengths'
        E=find(W);
        W(E)=1./W(E);           % invert weights
    case 'autofix'
        % clear diagonal
        n = length(W);
        W(1:n+1:end)=0;
        
        % remove Infs and NaNs
        idx = isnan(W) | isinf(W);
        if any(any(idx))
            W(idx)=0;
        end
        
        % ensure exact binariness
        U = unique(W);
        if nnz(U) > 1
            idx_0 = abs(W  ) < 1e-10;
            idx_1 = abs(W-1) < 1e-10;
            if all(all(idx_0 | idx_1))
                W(idx_0)=0;
                W(idx_1)=1;
            end
        end
        
        % ensure exact symmetry
        if ~isequal(W,W.')
            if max(max(abs(W-W.'))) < 1e-10
                W=(W+W).'/2;
            end
        end
    otherwise
        error('Unknown weight-conversion command.')
end
end

%node degree:
function [deg] = degrees_und(CIJ)
%DEGREES_UND        Degree
%
%   deg = degrees_und(CIJ);
%   Input:      CIJ,    undirected (binary/weighted) connection matrix
%   Output:     deg,    node degree
%   Olaf Sporns, Indiana University, 2002/2006/2008
CIJ = double(CIJ~=0);

deg = sum(CIJ);
end

%Strength:
function [str] = strengths_und(CIJ)
%STRENGTHS_UND       
%   str = strengths_und(CIJ);
%   Input:      CIJ,    undirected weighted connection matrix
%   Output:     str,    node strength
%   Olaf Sporns, Indiana University, 2002/2006/2008
str = sum(CIJ);        % strength
end

%Density:
function [kden,N,K] = density_und(CIJ)
% DENSITY_UND        Density
%   kden = density_und(CIJ);
%   [kden,N,K] = density_und(CIJ);
%   Input:      CIJ,    undirected (weighted/binary) connection matrix
%   Output:     kden,   density
%               N,      number of vertices
%               K,      number of edges
%   Olaf Sporns, Indiana University, 2002/2007/2008
N = size(CIJ,1);
K = nnz(triu(CIJ));
kden = K/((N^2-N)/2);
end

%Clustering coefficient:
function C=clustering_coef_wu(W)
%CLUSTERING_COEF_WU   
%   C = clustering_coef_wu(W);
%   The weighted clustering coefficient is the average "intensity"
%   (geometric mean) of all triangles associated with each node.
%   Input:      W,      weighted undirected connection matrix
%                       (all weights must be between 0 and 1)
%   Output:     C,      clustering coefficient vector
%   Reference: Onnela et al. (2005) Phys Rev E 71:065103
%   Mika Rubinov, UNSW/U Cambridge, 2007-2015
%   Modification history:
%   2007: original
%   2015: expanded documentation

K=sum(W~=0,2);            	
cyc3=diag((W.^(1/3))^3);           
K(cyc3==0)=inf;             %if no 3-cycles exist, make C=0 (via K=inf)
C=cyc3./(K.*(K-1));         %clustering coefficient
end

%Global and local efficiency:
function E = efficiency_wei(W, local)
%EFFICIENCY_WEI     Global efficiency, local efficiency.
%
%   Eglob = efficiency_wei(W);
%   Eloc = efficiency_wei(W,2);
%   Inputs:     W,
%                   weighted undirected or directed connection matrix
%
%               local,
%                   optional argument
%                   local=0  computes the global efficiency (default).
%                  	local=1  computes the original version of the local
%                               efficiency.
%               	local=2  computes the modified version of the local
%                               efficiency (recommended, see below). 
%
%   Output:     Eglob,
%                   global efficiency (scalar)
%               Eloc,
%                   local efficiency (vector)
%
%   Notes:
%       The  efficiency is computed using an auxiliary connection-length
%   matrix L, defined as L_ij = 1/W_ij for all nonzero L_ij; This has an
%   intuitive interpretation, as higher connection weights intuitively
%   correspond to shorter lengths.
%       The weighted local efficiency broadly parallels the weighted
%   clustering coefficient of Onnela et al. (2005) and distinguishes the
%   influence of different paths based on connection weights of the
%   corresponding neighbors to the node in question. In other words, a path
%   between two neighbors with strong connections to the node in question
%   contributes more to the local efficiency than a path between two weakly
%   connected neighbors. Note that the original weighted variant of the
%   local efficiency (described in Rubinov and Sporns, 2010) is not a
%   true generalization of the binary variant, while the modified variant
%   (described in Wang et al., 2016) is a true generalization.
%       For ease of interpretation of the local efficiency it may be
%   advantageous to rescale all weights to lie between 0 and 1.
%
%   Algorithm:  Dijkstra's algorithm
%
%   References: Latora and Marchiori (2001) Phys Rev Lett 87:198701.
%               Onnela et al. (2005) Phys Rev E 71:065103
%               Fagiolo (2007) Phys Rev E 76:026107.
%               Rubinov M, Sporns O (2010) NeuroImage 52:1059-69
%               Wang Y et al. (2016) Neural Comput 21:1-19.
%
%   Mika Rubinov, U Cambridge/Janelia HHMI, 2011-2017

%Modification history
% 2011: Original (based on efficiency.m and distance_wei.m)
% 2013: Local efficiency generalized to directed networks
% 2017: Added the modified local efficiency and updated documentation.

n = length(W);                                              % number of nodes
ot = 1 / 3;                                                 % one third

L = W;                                                      % connection-length matrix
A = W > 0;                                                  % adjacency matrix
L(A) = 1 ./ L(A);
A = double(A);

if exist('local','var') && local                            % local efficiency
    E = zeros(n, 1);
    cbrt_W = W.^ot;
    switch local
        case 1
            for u = 1:n
                V  = find(A(u, :) | A(:, u).');             % neighbors
                sw = cbrt_W(u, V) + cbrt_W(V, u).';       	% symmetrized weights vector
                di = distance_inv_wei(L(V, V));             % inverse distance matrix
                se = di.^ot + di.'.^ot;                     % symmetrized inverse distance matrix
                numer = (sum(sum((sw.' * sw) .* se)))/2;   	% numerator
                if numer~=0
                    sa = A(u, V) + A(V, u).';              	% symmetrized adjacency vector
                    denom = sum(sa).^2 - sum(sa.^2);        % denominator
                    E(u) = numer / denom;                   % local efficiency
                end
            end
        case 2
            cbrt_L = L.^ot;
            for u = 1:n
                V  = find(A(u, :) | A(:, u).');            	% neighbors
                sw = cbrt_W(u, V) + cbrt_W(V, u).';       	% symmetrized weights vector
                di = distance_inv_wei(cbrt_L(V, V));      	% inverse distance matrix
                se = di + di.';                             % symmetrized inverse distance matrix
                numer=(sum(sum((sw.' * sw) .* se)))/2;      % numerator
                if numer~=0
                    sa = A(u, V) + A(V, u).';             	% symmetrized adjacency vector
                    denom = sum(sa).^2 - sum(sa.^2);        % denominator
                    E(u) = numer / denom;                 	% local efficiency
                end
            end
    end
else
    di = distance_inv_wei(L);
    E = sum(di(:)) ./ (n^2 - n);                         	% global efficiency
end
end

function D=distance_inv_wei(W_)

n_=length(W_);
D=inf(n_);                                                  % distance matrix
D(1:n_+1:end)=0;

for u=1:n_
    S=true(1,n_);                                           % distance permanence (true is temporary)
    W1_=W_;
    V=u;
    while 1
        S(V)=0;                                             % distance u->V is now permanent
        W1_(:,V)=0;                                         % no in-edges as already shortest
        for v=V
            T=find(W1_(v,:));                               % neighbours of shortest nodes
            D(u,T)=min([D(u,T);D(u,v)+W1_(v,T)]);           % smallest of old/new path lengths
        end
        
        minD=min(D(u,S));
        if isempty(minD)||isinf(minD)                       % isempty: all nodes reached;
            break,                                          % isinf: some nodes cannot be reached
        end;
        
        V=find(D(u,:)==minD);
    end
end

D=1./D;                                                     % invert distance
D(1:n_+1:end)=0;
end %esto no sé bien qué es

%Distance matrix:
function [D,B]=distance_wei(L)
% DISTANCE_WEI       Distance matrix (Dijkstra's algorithm)
%
%   D = distance_wei(L);
%   [D,B] = distance_wei(L);
%
%   The distance matrix contains lengths of shortest paths between all
%   pairs of nodes. An entry (u,v) represents the length of shortest path 
%   from node u to node v. The average shortest path length is the 
%   characteristic path length of the network.
%
%   Input:      L,      Directed/undirected connection-length matrix.
%   *** NB: The length matrix L isn't the weights matrix W (see below) ***
%
%   Output:     D,      distance (shortest weighted path) matrix
%               B,      number of edges in shortest weighted path matrix
%
%   Notes:
%       The input matrix must be a connection-length matrix, typically
%   obtained via a mapping from weight to length. For instance, in a
%   weighted correlation network higher correlations are more naturally
%   interpreted as shorter distances and the input matrix should
%   consequently be some inverse of the connectivity matrix. 
%       The number of edges in shortest weighted paths may in general 
%   exceed the number of edges in shortest binary paths (i.e. shortest
%   paths computed on the binarized connectivity matrix), because shortest 
%   weighted paths have the minimal weighted distance, but not necessarily 
%   the minimal number of edges.
%       Lengths between disconnected nodes are set to Inf.
%       Lengths on the main diagonal are set to 0.
%
%   Algorithm: Dijkstra's algorithm.
%
%
%   Mika Rubinov, UNSW/U Cambridge, 2007-2012.
%   Rick Betzel and Andrea Avena, IU, 2012

%Modification history
%2007: original (MR)
%2009-08-04: min() function vectorized (MR)
%2012: added number of edges in shortest path as additional output (RB/AA)
%2013: variable names changed for consistency with other functions (MR)

n=length(L);
D=inf(n);
D(1:n+1:end)=0;                             %distance matrix
B=zeros(n);                                 %number of edges matrix

for u=1:n
    S=true(1,n);                            %distance permanence (true is temporary)
    L1=L;
    V=u;
    while 1
        S(V)=0;                             %distance u->V is now permanent
        L1(:,V)=0;                          %no in-edges as already shortest
        for v=V
            T=find(L1(v,:));                %neighbours of shortest nodes
            [d,wi]=min([D(u,T);D(u,v)+L1(v,T)]);
            D(u,T)=d;                       %smallest of old/new path lengths
            ind=T(wi==2);                   %indices of lengthened paths
            B(u,ind)=B(u,v)+1;              %increment no. of edges in lengthened paths
        end

        minD=min(D(u,S));
        if isempty(minD)||isinf(minD)       %isempty: all nodes reached;
            break,                          %isinf: some nodes cannot be reached
        end;

        V=find(D(u,:)==minD);
    end
end
end

%Betweenness centrality:
function BC=betweenness_wei(G)
%BETWEENNESS_WEI    Node betweenness centrality
%
%   BC = betweenness_wei(L);
%
%   Node betweenness centrality is the fraction of all shortest paths in 
%   the network that contain a given node. Nodes with high values of 
%   betweenness centrality participate in a large number of shortest paths.
%
%   Input:      L,      Directed/undirected connection-length matrix.
%
%   Output:     BC,     node betweenness centrality vector.
%
%   Notes:
%       The input matrix must be a connection-length matrix, typically
%   obtained via a mapping from weight to length. For instance, in a
%   weighted correlation network higher correlations are more naturally
%   interpreted as shorter distances and the input matrix should
%   consequently be some inverse of the connectivity matrix. 
%       Betweenness centrality may be normalised to the range [0,1] as
%   BC/[(N-1)(N-2)], where N is the number of nodes in the network.
%
%   Reference: Brandes (2001) J Math Sociol 25:163-177.
%
%
%   Mika Rubinov, UNSW/U Cambridge, 2007-2012

n=length(G);
% E=find(G); G(E)=1./G(E);        %invert weights
BC=zeros(n,1);                  %vertex betweenness

for u=1:n
    D=inf(1,n); D(u)=0;         %distance from u
    NP=zeros(1,n); NP(u)=1;     %number of paths from u
    S=true(1,n);                %distance permanence (true is temporary)
    P=false(n);                 %predecessors
    Q=zeros(1,n); q=n;          %order of non-increasing distance

    G1=G;
    V=u;
    while 1
        S(V)=0;                 %distance u->V is now permanent
        G1(:,V)=0;              %no in-edges as already shortest
        for v=V
            Q(q)=v; q=q-1;
            W=find(G1(v,:));                %neighbours of v
            for w=W
                Duw=D(v)+G1(v,w);           %path length to be tested
                if Duw<D(w)                 %if new u->w shorter than old
                    D(w)=Duw;
                    NP(w)=NP(v);            %NP(u->w) = NP of new path
                    P(w,:)=0;
                    P(w,v)=1;               %v is the only predecessor
                elseif Duw==D(w)            %if new u->w equal to old
                    NP(w)=NP(w)+NP(v);      %NP(u->w) sum of old and new
                    P(w,v)=1;               %v is also a predecessor
                end
            end
        end

        minD=min(D(S));
        if isempty(minD), break             %all nodes reached, or
        elseif isinf(minD)                  %...some cannot be reached:
            Q(1:q)=find(isinf(D)); break	%...these are first-in-line
        end
        V=find(D==minD);
    end

    DP=zeros(n,1);                          %dependency
    for w=Q(1:n-1)
        BC(w)=BC(w)+DP(w);
        for v=find(P(w,:))
            DP(v)=DP(v)+(1+DP(w)).*NP(v)./NP(w);
        end
    end
end
end