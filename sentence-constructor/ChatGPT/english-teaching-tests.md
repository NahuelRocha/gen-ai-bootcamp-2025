# Documenting AI Behavior in Sentence Translation

```xml
<test-cases>
    ## 1. **Simple Sentences**
    <case id="simple-1">
        <english>El perro corre por el parque.</english>
        <vocabulary>
            <word>
                <spanish>perro</spanish>
                <english>dog</english>
            </word>
            <word>
                <spanish>correr</spanish>
                <english>run</english>
            </word>
            <word>
                <spanish>parque</spanish>
                <english>park</english>
            </word>
        </vocabulary>
        <structure>[Subject] [Verb] [Preposition] [Object]</structure>
        <considerations>
            - The sentence follows a simple subject-verb-object structure in both languages.
            - The preposition "en" is translated as "in", but there could be an alternative translation depending on whether the park is seen as an enclosed area.
            - "Runs" can be translated in the present tense, but if the action is ongoing, the present continuous "is running" might be more appropriate.
        </considerations>
    </case>
    ## 1. **Compound Sentences**
    <case id="compound-1">
        <english>Voy al cine y luego ceno en un restaurante.</english>
        <vocabulary>
            <word>
                <spanish>ir</spanish>
                <english>go</english>
            </word>
            <word>
                <spanish>cine</spanish>
                <english>cinema</english>
            </word>
            <word>
                <spanish>cenar</spanish>
                <english>dinner</english>
            </word>
            <word>
                <spanish>restaurante</spanish>
                <english>restaurant</english>
            </word>
        </vocabulary>
        <structure>[Subject] [Verb] [Preposition] [Object] [Conjunction] [Subject] [Verb] [Preposition] [Object]</structure>
        <considerations>
            - "Voy" translates as "go", but the verb tense must match the context (present or future).
            - "Después" can be translated as "after", but there are several ways to structure the sentence depending on the flow.
            - The conjunction "y" is translated as "and", while "después" is usually "then" or "after", depending on the emphasis.
        </considerations>
    </case>
    <case id="compound-2">
        <english>Estudio por la mañana, pero trabajo por la tarde.</english>
        <vocabulary>
            <word>
                <spanish>estudiar</spanish>
                <english>study</english>
            </word>
            <word>
                <spanish>mañana</spanish>
                <english>morning</english>
            </word>
            <word>
                <spanish>trabajar</spanish>
                <english>work</english>
            </word>
            <word>
                <spanish>tarde</spanish>
                <english>afternoon</english>
            </word>
        </vocabulary>
        <structure>[Subject] [Verb] [Preposition] [Object], [Conjunction] [Subject] [Verb] [Preposition] [Object]</structure>
        <considerations>
            - The conjunction "pero" is translated as "but", connecting two contrasting actions.
            - "En la mañana" and "en la tarde" are translated as "in the morning" and "in the afternoon."
        </considerations>
    </case>
    ## 1. **Complex Sentences**
    <case id="complex-1">
        <english>Si estudias mucho, aprobarás el examen.</english>
        <vocabulary>
            <word>
                <spanish>estudiar</spanish>
                <english>study</english>
            </word>
            <word>
                <spanish>aprobar</spanish>
                <english>pass</english>
            </word>
            <word>
                <spanish>examen</spanish>
                <english>exam</english>
            </word>
        </vocabulary>
        <structure>[If] [Subject] [Verb] [Object], [Subject] [Verb] [Object]</structure>
        <considerations>
            - "Si" translates as "If" and introduces the conditional phrase.
            - "Aprobar" is commonly translated as "pass the exam" to specify the object.
            - The structure of the sentence emphasizes the condition (study a lot) followed by the result (pass the exam).
        </considerations>
    </case>
     <case id="complex-2">
        <english>Si trabajo mucho, ganaré más dinero.</english>
        <vocabulary>
            <word>
                <spanish>trabajar</spanish>
                <english>work</english>
            </word>
            <word>
                <spanish>ganar</spanish>
                <english>earn</english>
            </word>
            <word>
                <spanish>dinero</spanish>
                <english>money</english>
            </word>
        </vocabulary>
        <structure>[If] [Subject] [Verb] [Object], [Subject] [Verb] [Object]</structure>
        <considerations>
            - The same conditional structure applies here as in the previous example.
            - "Ganar" is commonly translated as "earn" in this context, specifying the object "more money."
        </considerations>
    </case>
</test-cases>
```
