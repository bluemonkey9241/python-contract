import numpy as np
import matplotlib.pyplot as plt
from numeric_parameter import NumericParameter
from numeric_list_parameter import NumericListParameter


"""
Model for Money Supply given a Business Plan

"""


def nolinspace(xi, xf, n, eta):
    """No linear equal spacing of n values between xi and xf
    with curvature eta """
    x = np.linspace(1, n, n)
    y = ((x-1)/(n-1))**eta*(xf-xi)+xi
    return y


def get_numeric_parameters():
    return [
        NumericParameter('mu_u', '&mu; (users)', 0.3, 0.0, 1.0, True, True),
        NumericParameter('sigma_u', '&sigma; (users)',
                         0.15, 0.01, 0.9, True, True),
        NumericParameter('eta_u', '&eta; (users)',
                         100000000.0, 0, 200000000.0, True, True),
        NumericParameter('muf', '&mu; (firms)', 0.4, 0.0, 1.0, True, True),
        NumericParameter('sigmaf', '&sigma; (firms)',
                         0.05, 0.01, 0.9, True, True),
        NumericParameter('eta_f', '&eta; (firms)',
                         2000000.0, 0.0, 5000000.0, True, True),
        NumericParameter('beta', 'Investors discount (&beta;)', 0.96, 0.9,
                         0.99, True, True),
        NumericParameter('fee', 'API Fees euros', 0.0025, 0.0023, 0.0028,
                         True, True),
    ]


def get_numeric_list_parameters():
    return [
        NumericListParameter('sGlobalCorp', 'Share Global Corp',
                             [0, 0, 0, 0, 0, 0.001, 0.004, 0.004, 0.004,
                              0.004, 0.004, 0.004, 0.004, 0.004]),
        NumericListParameter('sMulti', 'Share Multinational',
                             [0, 0, 0, 0, 0, 0.005, 0.03, 0.03, 0.03,
                              0.03, 0.03, 0.03, 0.03, 0.03]),
        NumericListParameter('sBig', 'Share Big',
                             [0, 0, 1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6]),
        NumericListParameter('sMid', 'Share Mid',
                             [0, 0, 4, 4, 4, 10, 10, 10, 10, 10, 10, 10,
                              10, 12]),
        NumericListParameter('sSmall', 'Share Small',
                             [0, 10, 15, 25, 35, 45, 45, 45, 45, 45, 45, 45,
                              45, 45]),
        NumericListParameter('sStartUp', 'Share Startups',
                             [100, 90, 80, 70, 60, 50, 41, 41, 41, 41, 41, 41,
                              41, 41]),
        NumericListParameter('dGlobalCorp', 'Discount Global Corps',
                             [0, 0, 0, 0, 0, 1, 9, 31, 65, 75, 79, 80,
                              80, 80]),
        NumericListParameter('dMulti', 'Discount Multinationals',
                             [0, 0, 0, 0, 0, 3, 69, 231, 484, 565, 590, 597,
                              599, 600]),
        NumericListParameter('dBig', 'Discount Big',
                             [0, 0, 0, 30, 40, 50, 60, 70, 80, 80, 80, 80,
                              80, 80]),
        NumericListParameter('dMid', 'Discount Mid',
                             [0, 0, 0, 50, 70, 85, 92, 97, 97, 97, 97, 97,
                              97, 97]),
        NumericListParameter('dSmall', 'Discount Small',
                             [0, 0, 0, 50, 70, 85, 92, 97, 97, 97, 97, 97,
                              97, 97]),
        NumericListParameter('dStartUp', 'Discount Startups',
                             [0, 0, 50, 80, 90, 96, 98.5, 99.4, 99.4, 99.4,
                              99.4, 99.4, 99.4, 99.4]),
        ]


def money_supply(mu_u=0.3, sigma_u=0.08, eta_u=100000000.0, muf=0.5,
                 sigmaf=0.05, eta_f=2000000.0, beta=0.96, fee=0.0025,
                 sGlobalCorp=[], sMulti=[], sBig=[], sMid=[], sSmall=[],
                 sStartUp=[], dGlobalCorp=[], dMulti=[], dBig=[], dMid=[],
                 dSmall=[], dStartUp=[]):
    # Initialize all arrays
    fsGlobalCorp = np.zeros(len(sGlobalCorp))
    fsMulti = np.zeros(len(sGlobalCorp))
    fsBig = np.zeros(len(sGlobalCorp))
    fsMid = np.zeros(len(sGlobalCorp))
    fsSmall = np.zeros(len(sGlobalCorp))
    fsStartUp = np.zeros(len(sGlobalCorp))
    dGlobalCorp = np.zeros(len(sGlobalCorp))
    dMulti = np.zeros(len(sGlobalCorp))
    dBig = np.zeros(len(sGlobalCorp))
    dMid = np.zeros(len(sGlobalCorp))
    dSmall = np.zeros(len(sGlobalCorp))
    dStartUp = np.zeros(len(sGlobalCorp))
    iGlobalCorp = np.zeros(len(sGlobalCorp))
    iMulti = np.zeros(len(sGlobalCorp))
    iBig = np.zeros(len(sGlobalCorp))
    iMid = np.zeros(len(sGlobalCorp))
    iSmall = np.zeros(len(sGlobalCorp))
    iStartUp = np.zeros(len(sGlobalCorp))
    PDV = np.zeros(14+50, dtype='float')

    # Cast strings into floats
    for item in range(len(sGlobalCorp)):
        fsGlobalCorp[item] = float(sGlobalCorp[item])
        fsMulti[item] = float(sMulti[item])
        fsBig[item] = float(sBig[item])
        fsMid[item] = float(sMid[item])
        fsSmall[item] = float(sSmall[item])
        fsStartUp[item] = (100-fsGlobalCorp[item]-fsMulti[item]-fsBig[item]
                           - fsMid[item]-fsSmall[item])

    T = 100
    Tcomp = len(sGlobalCorp)
    y = np.linspace(0.0, 1.0, num=Tcomp)
    x = np.linspace(0.0, 1.0, num=T)
    AxPlot = eta_u*((1/2) + 1*np.sign(x-mu_u)/2*(1-np.exp(-np.sqrt(2)/sigma_u
                                                          * np.abs(x-mu_u))))
    FxPlot = eta_f*((1/2) + 1*np.sign(x-muf)/2*(1-np.exp(-np.sqrt(2)/sigmaf
                                                         * np.abs(x-muf))))
    AxComp = eta_u*((1/2) + 1*np.sign(y-mu_u)/2*(1-np.exp(-np.sqrt(2)/sigma_u
                                                          * np.abs(y-mu_u))))
    FxComp = eta_f*((1/2) + 1*np.sign(y-muf)/2*(1-np.exp(-np.sqrt(2)/sigmaf
                                                         * np.abs(y-muf))))

    for item in range(len(sGlobalCorp)):
        iGlobalCorp[item] = (fee*(1-dGlobalCorp[item])*fsGlobalCorp[item]
                             * FxComp[item] * AxComp[item])
        iMulti[item] = (fee*(1-dMulti[item])*fsMulti[item] * FxComp[item]
                        * AxComp[item])
        iBig[item] = (fee*(1-dBig[item])*fsBig[item] * FxComp[item]
                      * AxComp[item])
        iMid[item] = (fee*(1-dMid[item])*fsMid[item] * FxComp[item]
                      * AxComp[item])
        iSmall[item] = (fee*(1-dSmall[item])*fsSmall[item] * FxComp[item]
                        * AxComp[item])
        iStartUp[item] = (fee*(1-dStartUp[item])*fsStartUp[item] * FxComp[item]
                          * AxComp[item])

    iTotal = iGlobalCorp + iMulti + iBig + iMid + iSmall + iStartUp
    # iTotalMatrix = np.ones([14, 14+50], dtype='float')
    finalValue = iTotal[-1]*np.ones(50)
    iTotalFinalValue = np.hstack((iTotal, finalValue))
    for t in range(len(iTotalFinalValue)):
        PDV[t] = beta**t*iTotalFinalValue[t]

    SPDV = np.sum(PDV)
    print(SPDV)
    anos = [2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031,
            2032, 2033, 2034]
    q = np.zeros(T)
    qReturn = np.zeros(T-1)
    qinit = 100
    q[0] = qinit
    qr = 1.09  # Revaluation rate
    cnt = 1 - 1 / qr  # Constant to guarrantee that q(T) = 1
    for t in list(range(T - 1)):
        q[t + 1] = q[t] / qr + cnt
    for t in list(range(1, T)):
        qReturn[t - 1] = q[t - 1] / q[t]

    # Construct the payoff matrix
    icTotal = np.concatenate([iTotal, np.ones(50)*iTotal[-1]])
    VAN = np.zeros(1, dtype='float')
    element = np.zeros(len(icTotal))
    for t in range(len(icTotal)):
        element[t] = beta**t * icTotal[t]
        VAN = VAN + element[t]
    print(VAN)
    # Net Discounted Value at rate beta

    # Single subplot
    fig1, ax = plt.subplots()
    ax.plot(x, AxPlot)
    ax.set(xlabel='time', ylabel='Percentage', title='Adoption curve')
    ax.grid()
    fig1_txt = "The Adoption Curve is a formal representation of the" \
        "busines plan designed by Neiblock."
    fig1.savefig("Adoption.png")

    # Two subplots, unpack the axes array immediately
    fig2, (ax1, ax2) = plt.subplots(1, 2, sharey='none')
    ax1.plot(x, FxPlot)
    ax1.set_title("Firm's adoption")
    ax1.yaxis.grid(which="major", color='k', linestyle='-.', linewidth=0.7)
    ax2.plot(x, AxPlot)
    ax2.set_title("User's Adoption")
    ax2.yaxis.grid(which="major", color='k', linestyle='-.', linewidth=0.7)
    fig2_txt = "These two graphs represent User's adoption and firm's adoption"

    fig2.savefig("Costs.png")

    # Two subplots, the axes array is 1-d
    fig3, axarr = plt.subplots(2, sharex='none')
    axarr[0].plot(anos, iTotal)
    axarr[0].set_title("Vectoria's total income")
    axarr[0].yaxis.grid(which="major", color='k', linestyle='-.',
                        linewidth=0.7)
    axarr[1].plot(x, q)
    axarr[1].set_title("Pela exchange rate")
    axarr[1].yaxis.grid(which="major", color='k', linestyle='-.',
                        linewidth=0.7)
    fig3_txt = "Once the business plan is given and a pricing and rewards" \
        "policy is defined, the economics model" \
        "produces as an output a valuation for the token over time and" \
        "the monetary policy that sustain the projected revaluation."
    fig3.savefig("Money.png")

    fig4, ax = plt.subplots()
    ax.plot(x[0:T-1], qReturn)
    ax.plot(x, (1 / beta) * np.ones(T))
    ax.set(xlabel='time', ylabel='Percentage', title='Return rate and 1/beta')
    ax.grid()
    fig4_txt = "A ratio of exchange rates gives us the interest rate" \
        "received by holding pelas. There are several benchmark values:" \
        "Beta  tells us when collectors decide to get rid of their pelas." \
        "Other rates like IBEX return, tell us when investors do" \
        "want to undo their token holdings."
    plt.show()

    return [
        [fig1, fig1_txt],
        [fig2, fig2_txt],
        [fig3, fig3_txt],
        [fig4, fig4_txt],
    ]
