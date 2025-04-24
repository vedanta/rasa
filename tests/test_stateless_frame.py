def test_stateless_frame_llm(monkeypatch):
    from rasa.frames import stateless_frame
    from rasa.frames.stateless_frame import StatelessFrame

    # Patch where the function is used, not where it's defined!
    monkeypatch.setattr(stateless_frame, "call_llm", lambda prompt, **kwargs: "FAKE LLM OUTPUT: " + prompt)

    frame = StatelessFrame(name="stateless")
    state = {"user_input": "Tell me a travel tip"}
    result = frame.run(state)
    assert result["output"].startswith("FAKE LLM OUTPUT:")
    assert result["context"]["intent"] == "travel_request"
