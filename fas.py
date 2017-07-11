def fas():
    from syntaxnet_wrapper.wrapper_subprocess import SyntaxNetWrapperSubprocess as sws

    sn_wrapper = sws()



    print(sn_wrapper.parse_sentence("Bob brought a pizza to Alice"))


fas()