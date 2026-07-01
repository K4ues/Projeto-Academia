import os
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from habitusapp.forms import (
    AlunoForm,
    ProgressoForm,
    TreinoFormEdit,
    TreinoExercicioFormSet,
    SolicitacaoDeTreinoForm,
)
from habitusapp.models import (
    Aluno,
    Exercicio,
    Notificacao,
    Professor,
    Progresso,
    SolicitacaoDeTreino,
    Treino,
    TreinoExercicio,
    Noticia,
)


def get_user_profile(user):
    if hasattr(user, 'aluno'):
        return user.aluno
    if hasattr(user, 'professor'):
        return user.professor
    if hasattr(user, 'admin'):
        return user.admin
    return None


def get_profile_name(user):
    profile = get_user_profile(user)
    if profile and hasattr(profile, 'nome'):
        return profile.nome
    return user.username


def has_unread_notifications(user):
    return user.is_authenticated and Notificacao.objects.filter(usuario=user, lida=False).exists()


@csrf_protect
@require_POST
def logout_view(request):
    """View customizada de logout com proteção CSRF"""
    auth_logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('login')


@csrf_protect
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Usuário com este e-mail não existe!')
            return render(request, 'PagsUsuario/login.html')

        if not user_obj.is_active:
            messages.error(request, 'Sua conta está inativa. Entre em contato com a administração.')
            return render(request, 'PagsUsuario/login.html')

        user = authenticate(request, username=user_obj.username, password=senha)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login feito com sucesso!')
            return redirect('feed')

        else:
            messages.error(request, 'Senha incorreta! Tente novamente.')
            return render(request, 'PagsUsuario/login.html')

    return render(request, 'PagsUsuario/login.html')

@csrf_protect
def criar_conta(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')
    else:
        form = AlunoForm()
    
    return render(request, 'PagsUsuario/criar_conta.html', {'form': form})

@login_required
def feed(request):
    tem_notificacao = False
    if request.user.is_authenticated:
        tem_notificacao = Notificacao.objects.filter(usuario=request.user, lida=False).exists()
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    
    nome = None
    if hasattr(request.user, 'aluno'):
        nome = request.user.aluno.nome
    elif hasattr(request.user, 'professor'):
        nome = request.user.professor.nome
    elif hasattr(request.user, 'admin'):
        nome = request.user.admin.nome
    else:
        nome = request.user.username

    treino_do_dia = None
    treinos_usuario = Treino.objects.filter(usuario=request.user).order_by('id')
    if treinos_usuario.exists():
        progresso_obj = Progresso.objects.filter(usuario=request.user).first()
        ultimo_id = getattr(progresso_obj, 'ultimo_treino_id', None) if progresso_obj else None

        if ultimo_id:
            try:
                idx = list(treinos_usuario.values_list('id', flat=True)).index(ultimo_id)
                proximo_idx = (idx + 1) % treinos_usuario.count()
                treino_do_dia = treinos_usuario[proximo_idx]
            except ValueError:
                treino_do_dia = treinos_usuario.first()
        else:
            treino_do_dia = treinos_usuario.first()

    return render(request, 'PagsUsuario/feed.html', {
        'noticias': noticias,
        'nome_usuario': nome,
        'tem_notificacao': tem_notificacao,
        'treino_do_dia': treino_do_dia,
    })


@login_required
def treinos(request):
    progresso_total = calcular_progresso(request.user)
    progresso_obj = Progresso.objects.filter(usuario=request.user).first()
    concluidos = progresso_obj.concluidos if progresso_obj else 0
    faltando = progresso_total - concluidos if progresso_total > concluidos else 0
    tem_notificacao = has_unread_notifications(request.user)
    treinos_usuario = Treino.objects.filter(usuario=request.user,arquivado=False).order_by('-id')
    

    return render(request, 'PagsUsuario/treinos.html', {
        'treinos_usuario': treinos_usuario,
        'tem_notificacao': tem_notificacao,
        'total': progresso_total,
        'concluidos': concluidos,
        'faltando': faltando,
    })

def detalhes_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id)
    montador = treino.usuario.get_full_name() or treino.usuario.username
    professor = treino.professor.nome if treino.professor else None
    exercicios = []
    for te in TreinoExercicio.objects.filter(treino=treino).select_related("exercicio"):
        exercicios.append({
            "nome": te.exercicio.nome,
            "imagem": te.exercicio.imagem.url if getattr(te.exercicio, "imagem", None) else None,
            "series": te.series,
            "repeticoes": te.repeticoes,
            "carga": te.carga if te.carga else "-",
            "observacao": te.observacao if te.observacao else "",
        })

    data = {
        "montador": montador,
        "professor": professor,
        "data_inicio": treino.data_inicio.strftime("%d/%m/%Y"),
        "data_fim": treino.data_fim.strftime("%d/%m/%Y"),
        "objetivo": getattr(treino, "objetivo", "Não informado"),  
        "nivel": treino.get_nivel_display(),
        "exercicios": exercicios,
    }
    return JsonResponse(data)




@login_required
def meus_dados(request):
    perfil = get_user_profile(request.user)
    return render(request, 'PagsUsuario/meus_dados.html', {'perfil': perfil})

@login_required
def perfil(request):
    tem_notificacao = False
    if request.user.is_authenticated:
        tem_notificacao = Notificacao.objects.filter(usuario=request.user, lida=False).exists()
    perfil = None

    if hasattr(request.user, 'aluno'):
        perfil = request.user.aluno
    elif hasattr(request.user, 'professor'):
        perfil = request.user.professor
    elif hasattr(request.user, 'admin'):
        perfil = request.user.admin

    return render(request, 'PagsUsuario/perfil.html', {
        'perfil': perfil,
        'tem_notificacao': tem_notificacao
        })

@login_required
def editar_perfil(request):
    user = request.user

    if hasattr(user, "aluno"):
        perfil = user.aluno
    elif hasattr(user, "professor"):
        perfil = user.professor
    elif hasattr(user, "admin"):
        perfil = user.admin
    else:
        messages.error(request, "Perfil não encontrado")
        return redirect("meus_dados")

    if request.method == "POST":
        nome = request.POST.get("nome")
        username = request.POST.get("username")
        email = request.POST.get("email")
        data_nasc = request.POST.get("data_nasc")
        telefone = request.POST.get("telefone")

        user.username = username
        user.email = email
        user.save()

        perfil.nome = nome
        perfil.data_nasc = data_nasc
        perfil.telefone = telefone
        perfil.save()

        messages.success(request, "Dados atualizados com sucesso!")
        return redirect("meus_dados")

    return render(request, "PagsUsuario/editar_perfil.html", {"perfil": perfil})

@login_required
def editar_foto(request):
    perfil = None

    if hasattr(request.user, 'aluno'):
        perfil = request.user.aluno
    elif hasattr(request.user, 'professor'):
        perfil = request.user.professor
    elif hasattr(request.user, 'admin'):
        perfil = request.user.admin

    if request.method == 'POST':
        if 'usar_foto_padrao' in request.POST:
            if perfil.foto_perfil and os.path.isfile(perfil.foto_perfil.path):
                os.remove(perfil.foto_perfil.path)
            perfil.foto_perfil = None
            perfil.save()
            Notificacao.objects.create(usuario=request.user, conteudo="Você alterou sua foto de perfil para a padrão")
            return redirect('perfil')

        elif 'nova_foto' in request.FILES:
            if perfil.foto_perfil and os.path.isfile(perfil.foto_perfil.path):
                os.remove(perfil.foto_perfil.path)
            perfil.foto_perfil = request.FILES['nova_foto']
            perfil.save()
            Notificacao.objects.create(usuario=request.user, conteudo="Você alterou sua foto de perfil")
            return redirect('perfil')

    return render(request, 'PagsUsuario/perfil.html', {'perfil': perfil})





@csrf_protect
@login_required
def novo_treino(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        nivel = request.POST.get('nivel')

        exercicios_ids = request.POST.getlist('exercicios')
        series = request.POST.getlist('series')
        repeticoes = request.POST.getlist('repeticoes')
        carga = request.POST.getlist('carga')
        observacoes = request.POST.getlist('observacoes')

        if not exercicios_ids:
            messages.error(request, "Você precisa adicionar pelo menos um exercício ao treino.")
            return redirect('novo_treino')

        for i in range(len(exercicios_ids)):
            if not series[i] or int(series[i]) <= 0:
                messages.error(request, f"O(s) exercício(s) precisa ter número de séries maior que 0.")
                return redirect('novo_treino')

            if not repeticoes[i] or int(repeticoes[i]) <= 0:
                messages.error(request, f"O(s) exercício(s) precisa ter número de repetições maior que 0.")
                return redirect('novo_treino')

            if not carga[i] or carga[i].strip() == "":
                messages.error(request, f"O(s) exercício(s) precisa ter carga definida.")
                return redirect('novo_treino')

        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

        treino = Treino.objects.create(
            nome=nome,
            data_inicio=data_inicio,
            data_fim=data_fim,
            nivel=nivel,
            usuario=request.user
        )

        Notificacao.objects.create(
            usuario=request.user,
            conteudo="Você criou um novo treino."
        )

        for i in range(len(exercicios_ids)):
            TreinoExercicio.objects.create(
                treino=treino,
                exercicio_id=exercicios_ids[i],
                series=int(series[i]),
                repeticoes=int(repeticoes[i]),
                carga=carga[i],
                observacao=observacoes[i] if observacoes else None
            )

        messages.success(request, 'Novo treino adicionado com sucesso!')
        return redirect('treinos')

    exercicios = Exercicio.objects.all()
    return render(request, 'PagsUsuario/novo_treino.html', {'exercicios': exercicios})


def buscar_exercicios(request):
    termo = request.GET.get("q", "").strip().lower()
    grupo = request.GET.get("grupo", "").strip()
    excluidos = request.GET.get("excluidos", "")
    excluidos_ids = [int(x) for x in excluidos.split(",") if x.isdigit()]

    exercicios = Exercicio.objects.all()

    if termo:
        exercicios = exercicios.filter(nome__icontains=termo)

    if grupo:
        exercicios = exercicios.filter(grupo_muscular__iexact=grupo)

    if excluidos_ids:
        exercicios = exercicios.exclude(id__in=excluidos_ids)

    exercicios = exercicios.distinct()[:10]

    data = []
    for e in exercicios:
        data.append({
            "id": e.id,
            "nome": e.nome,
            "grupo_muscular": e.grupo_muscular,
            "video_url": e.video.url if e.video else None
        })
    return JsonResponse(data, safe=False)



@login_required
def notificacoes(request):
    hoje = date.today()

    data_inicio = request.GET.get('data_inicio', hoje.strftime("%Y-%m-%d"))
    data_fim = request.GET.get('data_fim', hoje.strftime("%Y-%m-%d"))

    notificacoes = Notificacao.objects.filter(usuario=request.user)

    di = parse_date(data_inicio)
    df = parse_date(data_fim)
    if di and df:
        notificacoes = notificacoes.filter(data__date__range=[di, df])

    limite = timezone.now() - timedelta(hours=24)
    notificacoes.filter(lida=False, data__lte=limite).update(lida=True)

    notificacoes = notificacoes.order_by("-data")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("PagsUsuario/notificacoes.html", {
            "notificacoes": notificacoes,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        })
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        container_html = str(soup.select_one("#notificacoes-container"))
        return JsonResponse({"html": container_html})

    return render(request, "PagsUsuario/notificacoes.html", {
        "notificacoes": notificacoes,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    })


@csrf_protect
@login_required
def editar_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)

    if request.method == "POST":
        form = TreinoFormEdit(request.POST, instance=treino)
        formset = TreinoExercicioFormSet(request.POST, instance=treino)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Treino atualizado com sucesso!")
            Notificacao.objects.create(
            usuario=request.user,
            conteudo="Você editou seu treino com sucesso"
            )
            return redirect("treinos")
    else:
        form = TreinoFormEdit(instance=treino)
        formset = TreinoExercicioFormSet(instance=treino)

    return render(request, "PagsUsuario/editar_treino.html", {
        "form": form,
        "formset": formset,
        "treino": treino
    })


@csrf_protect
@login_required
def excluir_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)

    if request.method == "POST":
        treino.delete()
        messages.success(request, "Treino excluído com sucesso!")
        Notificacao.objects.create(
            usuario=request.user,
            conteudo="Você excluiu seu treino com sucesso"
            )
        return redirect("treinos")

    return redirect("treinos")

def editar_detalhes(request):
    if request.method == "POST":
        exercicio_id = request.POST.get("id")
        exercicio = get_object_or_404(TreinoExercicio, id=exercicio_id)

        exercicio.series = request.POST.get("series")
        exercicio.repeticoes = request.POST.get("repeticoes")
        exercicio.carga = request.POST.get("carga")
        exercicio.observacao = request.POST.get("observacao")
        exercicio.save()

        messages.success(request, "Exercício atualizado com sucesso!")
        next_url = request.POST.get("next", "/")
        return redirect(next_url)



def desenvolvedores(request):
    return render(request, 'PagsUsuario/desenvolvedores.html')

def politica_de_privacidade(request):
    return render(request, 'PagsUsuario/politica_de_privacidade.html')
def termos_de_uso(request):
    return render(request, 'PagsUsuario/termos_de_uso.html')

def sobre_habitus(request):
    return render(request, 'PagsUsuario/sobre_habitus.html')

def configuracoes(request):
    progresso_total = calcular_progresso(request.user)

    progresso_obj = Progresso.objects.filter(usuario=request.user).first()
    concluidos = progresso_obj.concluidos if progresso_obj else 0
    faltando = progresso_total - concluidos if progresso_total > concluidos else 0

    treinos_usuario = Treino.objects.filter(usuario=request.user).order_by('-id')
    total_treinos = treinos_usuario.count()

    return render(request, 'PagsUsuario/configuracoes.html', {
        'treinos_usuario': treinos_usuario,
        'total': progresso_total,
        'concluidos': concluidos,
        'faltando': faltando,
        'total_treinos':total_treinos,
    })


@csrf_protect
@login_required
def apagar_todos_treinos(request):
    if request.method == "POST":
        request.user.treino_set.all().delete() 
        messages.success(request, "Todos os seus treinos foram apagados com sucesso.")
        return redirect("configuracoes") 
    return redirect("configuracoes")



@csrf_protect
@login_required
def zerar_progresso(request):
    if request.method == "POST":
        progresso, _ = Progresso.objects.get_or_create(usuario=request.user)
        progresso.progresso_valor = 0
        progresso.concluidos = 0
        progresso.save()

        messages.success(request, "Seu progresso foi zerado com sucesso!")
        return redirect("configuracoes")
    return redirect("configuracoes")


@csrf_protect
@login_required
def comecar_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)
    exercicios = list(treino.exercicios_treino.all())
    
    index = int(request.GET.get('ex', 0))
    
    if index >= len(exercicios):
        return redirect(reverse('treino', args=[treino.id]))

    exercicio_atual = exercicios[index]

    proximo_exercicio = None
    if index + 1 < len(exercicios):
        proximo_exercicio = exercicios[index + 1]

    return render(request, 'PagsUsuario/treino.html', {
        'treino': treino,
        'exercicio_atual': exercicio_atual,
        'proximo_exercicio': proximo_exercicio, 
        'exercicio_index': index,
        'proximo_index': index + 1,
        'anterior_index': index - 1 if index > 0 else None,
        'total': len(exercicios)
    })


@require_POST
@login_required
def marcar_concluido(request, exercicio_id):
    exercicio = get_object_or_404(TreinoExercicio, id=exercicio_id, treino__usuario=request.user)
    exercicio.concluido = True
    messages.success(request, "Exercício marcado como concluído!")
    exercicio.save()
    return redirect(request.META.get('HTTP_REFERER', 'treino'))

@login_required
def finalizar_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)

    treino.exercicios_treino.update(concluido=False)

    progresso_obj = Progresso.objects.filter(usuario=request.user).first()
    if not progresso_obj:
        progresso_obj = Progresso.objects.create(usuario=request.user)

    if progresso_obj.concluidos < (progresso_obj.progresso_valor or 0):
        progresso_obj.concluidos += 1
        progresso_obj.ultimo_treino_id = treino.id
        progresso_obj.save()
        messages.success(request, "Treino finalizado com sucesso!")

        hoje_str = timezone.now().date().isoformat()
        nome_treino = getattr(treino, 'nome', None) or getattr(treino, 'titulo', None) or f"Treino {treino.id}"

        entry = {"date": hoje_str, "treino_id": treino.id, "nome": nome_treino}

        raw = progresso_obj.dias_treinados or []

        normalized = []
        for e in raw:
            if isinstance(e, str):
                normalized.append({"date": e, "treino_id": None, "nome": None})
            elif isinstance(e, dict):
                normalized.append(e)
            else:
                continue

        exists = any((d.get('date') == hoje_str and d.get('treino_id') == treino.id) for d in normalized)
        if not exists:
            normalized.append(entry)
            progresso_obj.dias_treinados = normalized
            progresso_obj.save()

    return HttpResponseRedirect(reverse('treinos'))



def calcular_progresso(usuario):
    treinos = Treino.objects.filter(usuario=usuario)
    total_treinos = treinos.count()

    if total_treinos == 0:
        progresso_total = 0
    else:
        soma_dias = 0
        for treino in treinos:
            dias = (treino.data_fim - treino.data_inicio).days
            soma_dias += dias

        progresso_total = round(soma_dias / total_treinos)

    progresso_obj = Progresso.objects.filter(usuario=usuario).first()
    
    if progresso_obj:
        progresso_obj.progresso_valor = progresso_total
        progresso_obj.save()
    else:
        progresso_obj = Progresso.objects.create(
            usuario=usuario,
            progresso_valor=progresso_total
        )

    return progresso_total



def solicitar_novo_treino(request, professor_id=None):
    user = request.user
    aba_ativa = request.GET.get('aba', 'professores')
    minhas_solicitacoes = SolicitacaoDeTreino.objects.filter(usuario=user)
    solicitacoes_alunos = None
    data_atual = date.today().isoformat()
    data_inicio = data_atual
    data_fim = data_atual
    situacao = 'A'
    data_inicio_alunos = data_atual
    data_fim_alunos = data_atual
    situacao_alunos = 'A'
    
    if aba_ativa == 'solicitacoes':
        data_inicio = request.GET.get('data_inicio', data_atual)
        data_fim = request.GET.get('data_fim', data_atual)
        situacao = request.GET.get('situacao', 'A')
        
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                minhas_solicitacoes = minhas_solicitacoes.filter(criado_em__date__gte=data_inicio_obj)
            except ValueError:
                pass
        
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                minhas_solicitacoes = minhas_solicitacoes.filter(criado_em__date__lte=data_fim_obj)
            except ValueError:
                pass
        
        if situacao and situacao in ['A', 'C', 'R']:
            minhas_solicitacoes = minhas_solicitacoes.filter(status=situacao)
        
        minhas_solicitacoes = minhas_solicitacoes.order_by('-criado_em')
        
    elif aba_ativa == 'solicitacoes-alunos' and user.is_authenticated and user.groups.filter(name="Professor").exists():
        data_inicio_alunos = request.GET.get('data_inicio_alunos', data_atual)
        data_fim_alunos = request.GET.get('data_fim_alunos', data_atual)
        situacao_alunos = request.GET.get('situacao_alunos', 'A')
        
        try:
            professor_logado = Professor.objects.get(user=user)
            solicitacoes_alunos = SolicitacaoDeTreino.objects.filter(professor=professor_logado)
            
            if data_inicio_alunos:
                try:
                    data_inicio_obj = datetime.strptime(data_inicio_alunos, '%Y-%m-%d').date()
                    solicitacoes_alunos = solicitacoes_alunos.filter(criado_em__date__gte=data_inicio_obj)
                except ValueError:
                    pass
            
            if data_fim_alunos:
                try:
                    data_fim_obj = datetime.strptime(data_fim_alunos, '%Y-%m-%d').date()
                    solicitacoes_alunos = solicitacoes_alunos.filter(criado_em__date__lte=data_fim_obj)
                except ValueError:
                    pass
            
            if situacao_alunos and situacao_alunos in ['A', 'C', 'R']:
                solicitacoes_alunos = solicitacoes_alunos.filter(status=situacao_alunos)
            
            solicitacoes_alunos = solicitacoes_alunos.order_by('-criado_em')
            
        except Professor.DoesNotExist:
            solicitacoes_alunos = None

    professores = Professor.objects.all().order_by('nome')
    
    context = {
        'professores': professores,
        'solicitacoes': minhas_solicitacoes,
        'solicitacoes_alunos': solicitacoes_alunos,
        'aba_ativa': aba_ativa,
        'data_inicio_selecionada': data_inicio,
        'data_fim_selecionada': data_fim,
        'situacao_selecionada': situacao,
        'data_inicio_selecionada_alunos': data_inicio_alunos,
        'data_fim_selecionada_alunos': data_fim_alunos,
        'situacao_selecionada_alunos': situacao_alunos,
        'data_atual': data_atual,
    }
    
    if professor_id is None:
        return render(request, 'PagsUsuario/solicitar_novo_treino.html', context)
    
    professor = get_object_or_404(Professor, pk=professor_id)
    if request.method == 'POST':
        if not user.is_authenticated:
            messages.error(request, "Você precisa estar logado para enviar uma solicitação.")
            return redirect('login')
        form = SolicitacaoDeTreinoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = user
            solicitacao.professor = professor
            solicitacao.save()
            messages.success(request, "Solicitação enviada com sucesso!")
            return redirect('solicitar_novo_treino')
    else:
        form = SolicitacaoDeTreinoForm()
    
    context['professor'] = professor
    context['form'] = form
    return render(request, 'PagsUsuario/professor_escolhido.html', context)


@login_required
def aceitar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoDeTreino, id=solicitacao_id)

    if request.user != solicitacao.professor.user:
        messages.error(request, "Você não tem permissão para essa ação.")
        return redirect('solicitar_novo_treino')

    solicitacao.status = 'C'
    solicitacao.save()
    messages.success(request, "Solicitação marcada como concluída.")
    return redirect('solicitar_novo_treino')


@login_required
def recusar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoDeTreino, id=solicitacao_id)

    if request.user != solicitacao.professor.user:
        messages.error(request, "Você não tem permissão para essa ação.")
        return redirect('solicitar_novo_treino')

    solicitacao.status = 'R'
    solicitacao.save()
    messages.success(request, "Solicitação recusada.")
    return redirect('solicitar_novo_treino')

@login_required
def redirecionar_treinos_por_usuario(request, user_id):
    aluno = Aluno.objects.filter(user_id=user_id).first()
    if aluno:
        return redirect('gerenciar_treinos', aluno_id=aluno.id)

    professor = Professor.objects.filter(user_id=user_id).first()
    if professor:
        return redirect('gerenciar_treinos', professor_id=professor.id)

    messages.error(request, "Não foi possível encontrar treinos associados a este usuário.")
    return redirect('feed')


def historico(request):
    if request.user.is_authenticated:
        treinos_arquivados = Treino.objects.filter(usuario=request.user, arquivado=True).order_by('-data_fim')
    else:
        treinos_arquivados = None

    return render(request, 'PagsUsuario/historico.html', {'treinos': treinos_arquivados})


def reportar_erro(request):
    return render(request, 'PagsUsuario/reportar_erro.html')

@login_required
def meu_progresso(request):
    progresso_total = calcular_progresso(request.user)
    hoje = timezone.now().date()

    inicio_semana = hoje - timedelta(days=hoje.weekday() + 1)
    fim_semana = inicio_semana + timedelta(days=6)

    progresso_obj = Progresso.objects.filter(usuario=request.user).first()
    raw = progresso_obj.dias_treinados if progresso_obj else []

    normalized = []
    for e in raw:
        if isinstance(e, str):
            normalized.append({"date": e, "treino_id": None, "nome": None})
        elif isinstance(e, dict):
            normalized.append(e)
        else:
            continue

    dates_with_training = {d.get('date') for d in normalized if d.get('date')}

    nomes = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]
    dias_semana = []
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        dia_str = dia.isoformat()
        dias_semana.append({
            "nome": nomes[i],
            "data": dia.day,
            "treinou": dia_str in dates_with_training
        })

    map_date = {}
    for e in normalized:
        d = e.get('date')
        if not d:
            continue
        try:
            d_obj = datetime.fromisoformat(d).date()
        except Exception:
            continue
        if inicio_semana <= d_obj <= fim_semana:
            map_date.setdefault(d, []).append(e)

    treinos_por_dia = []
    for date_str, entries in map_date.items():
        date_obj = datetime.fromisoformat(date_str).date()
        resolved = []
        for e in entries:
            nome = e.get('nome')
            if not nome and e.get('treino_id'):
                t = Treino.objects.filter(id=e.get('treino_id')).first()
                if t:
                    nome = getattr(t, 'nome', None) or getattr(t, 'titulo', None) or f"Treino {t.id}"
            if not nome:
                nome = "Treino finalizado"
            resolved.append({'nome': nome})
        treinos_por_dia.append({
            'date': date_obj,
            'entries': resolved,
            'count': len(resolved)
        })
    treinos_por_dia.sort(key=lambda x: x['date'])

    concluidos = progresso_obj.concluidos if progresso_obj else 0

    progressos = Progresso.objects.filter(usuario=request.user).order_by('-data_entrada')
    progresso_recente = progressos.first() if progressos else None

    data_selecionada = request.GET.get('data')
    progresso_filtrado = None
    if data_selecionada:
        try:
            progresso_filtrado = progressos.filter(data_entrada=data_selecionada).first()
        except:
            progresso_filtrado = None

    progresso_exibicao = progresso_filtrado if progresso_filtrado else progresso_recente
    datas_disponiveis = progressos.values_list('data_entrada', flat=True).distinct()

    return render(request, "PagsUsuario/meu_progresso.html", {
        "dias_semana": dias_semana,
        "total": progresso_total,
        "concluidos": concluidos,
        "treinos_por_dia": treinos_por_dia,
        "progresso": progresso_exibicao,
        "progressos": progressos,
        "datas_disponiveis": datas_disponiveis,
        "data_selecionada": data_selecionada,
    })


@login_required
def adicionar_meu_progresso(request):
    if request.method == 'POST':
        form = ProgressoForm(request.POST)
        if form.is_valid():
            novo_progresso = form.save(commit=False)
            novo_progresso.usuario = request.user
            novo_progresso.save()
            messages.success(request, 'Progresso adicionado com sucesso!')
            return redirect('meu_progresso')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ProgressoForm()
    
    context = {
        'form': form,
        'titulo': 'Adicionar Meu Progresso',
    }
    return render(request, 'PagsUsuario/adicionar_meu_progresso.html', context)

@login_required
def editar_meu_progresso(request, progresso_id):
    try:
        progresso = Progresso.objects.get(id=progresso_id, usuario=request.user)
    except Progresso.DoesNotExist:
        messages.error(request, 'Progresso não encontrado.')
        return redirect('meu_progresso')
    
    if request.method == 'POST':
        form = ProgressoForm(request.POST, instance=progresso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progresso atualizado com sucesso!')
            return redirect('meu_progresso')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ProgressoForm(instance=progresso)
    
    context = {
        'progresso': progresso,
        'form': form,
        'titulo': 'Editar Meu Progresso',
    }
    return render(request, 'PagsUsuario/editar_meu_progresso.html', context)

def get_or_create_progresso(usuario):
    """Função segura para obter ou criar Progresso, evitando MultipleObjectsReturned"""
    progresso = Progresso.objects.filter(usuario=usuario).first()
    if progresso:
        return progresso, False
    else:
        progresso = Progresso.objects.create(usuario=usuario)
        return progresso, True