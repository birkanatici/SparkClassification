import jpype


class zemberek:

    def __init__(self):

        jpype.startJVM("/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so",
                       "-Djava.class.path=./resources/zemberek-tum-2.0.jar", "-ea")
        Tr = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
        tr = Tr()
        Zemberek = jpype.JClass("net.zemberek.erisim.Zemberek")
        self.zemberek = Zemberek(tr)

    def kelime_cozumle(self, kelime):
        yanit = self.zemberek.kelimeCozumle(kelime)

        return yanit

    def kelime_kok(self, kelime):
        kok = kelime

        try:
            yanit = self.zemberek.kelimeCozumle(kelime)
            kok = yanit[0].kok().icerik()
        except:
            pass

        return kok

    def kelime_tip(self, kelime):
        tip = ""
        try:
            yanit = self.zemberek.kelimeCozumle(kelime)
            tip = yanit[0].kok().tip().name()
        except:
            pass
        return tip

    def jvm_kapat(self):

        jpype.shutdownJVM()
